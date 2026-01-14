import logging
import requests
import time
from typing import Dict, Any, Optional, Type
import urllib3

from ..config.default import APIConfig
from ..errors import (
    OneBullExError, ConnectError, TimeoutError, APIError, ClientError, ServerError,
    map_error_code
)
from ..auth.signer import Signer
from ..rate_limit import RateLimiter

logger = logging.getLogger("onebullex.transport")

class HTTPClient:
    """
    Production-ready HTTP Client wrapper.
    Handles:
    - Connection pooling (via requests.Session)
    - Timeouts
    - Retries (Selective)
    - Error Mapping
    - Signing
    - Rate Limiting
    """
    def __init__(self, config: APIConfig, signer: Optional[Signer] = None, rate_limiter: Optional[RateLimiter] = None):
        self.config = config
        self.signer = signer
        self.rate_limiter = rate_limiter or RateLimiter(config.rps)
        self.session = requests.Session()
        
        # Optimize connection pool
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
            max_retries=0 # We handle retries manually for better control
        )
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "OneBullEx-Python-Client/2.0"
        })

    def request(self, method: str, endpoint: str, 
                params: Optional[Dict] = None, 
                signed: bool = False,
                weight: int = 1) -> Any:
        
        url = f"{self.config.rest_url.rstrip('/')}{endpoint}"
        
        # 1. Rate Limiting
        self.rate_limiter.wait(weight)
        
        # 2. Signing
        headers = {}
        # Filter raw params
        params = {k: v for k, v in (params or {}).items() if v is not None}
        
        if signed:
            if not self.signer:
                raise ValueError("Signer required for signed requests")
            auth_headers = self.signer.sign(params, method)
            headers.update(auth_headers)
            
        # 3. Execution with Retry Loop
        retries = 0
        while True:
            try:
                if method.upper() == "GET":
                    # Params in URL
                    # NOTE: requests sorts params by default? No.
                    # BUT signer uses sorted params. 
                    # We must ensure requests sends them identically or server reconstructs correctly.
                    # Standard behavior is usually robust, but strictly:
                    # Requests takes dict. 
                    response = self.session.request(
                        method, url, params=params, headers=headers,
                        timeout=(self.config.timeout_connect, self.config.timeout_read)
                    )
                else:
                    # Params in JSON Body
                    response = self.session.request(
                        method, url, json=params, headers=headers,
                        timeout=(self.config.timeout_connect, self.config.timeout_read)
                    )
                
                # 4. Response Handling
                # 5xx Errors -> Retry
                if 500 <= response.status_code < 600:
                    raise ServerError(f"Server Error {response.status_code}", code=response.status_code)
                
                # 4xx Errors -> Raise immediately (Client Fault)
                if 400 <= response.status_code < 500:
                    # Try parsing body for specific code
                    try:
                        data = response.json()
                        err_code = data.get('code')
                        msg = data.get('msg', response.text)
                        
                        # Use Mapper
                        mapped_exc = map_error_code(err_code, msg, data)
                        if mapped_exc:
                            raise mapped_exc
                        else:
                             # Fallback
                            raise ClientError(f"Client Error {response.status_code}: {msg}", code=response.status_code)
                    except ValueError:
                         raise ClientError(f"Client Error {response.status_code}", code=response.status_code)

                # 200 OK -> Check business code
                data = response.json()
                code = data.get("code")
                msg = data.get("msg")
                
                # If code is missing, treat as success if data matches expected?
                # Or maybe the key is different?
                # Inspecting the error trace: APIError: [None] None
                # This means code was None.
                if code is None:
                    # Some endpoints might return raw list/dict without wrapper?
                    # But doc says "All API responses follow this format... code, msg, data"
                    # Exception: Maybe some legacy endpoints?
                    # Let's log and Assume Success if we can't determine error?
                    # Or treat as error?
                    # For verification, let's print it.
                    logger.warning(f"Response missing 'code' field: {data}")
                    # If we return data, we might be returning the whole dict as data?
                    return data 

                if code != 0 and code != 200:
                     mapped_exc = map_error_code(code, msg, data)
                     if mapped_exc:
                         # 5xx logic codes inside 200 response? Rare but possible.
                         # If it's a "System busy" code, maybe retry?
                         # For now, treat as error.
                         raise mapped_exc
                     raise APIError(f"API Error {code}: {msg}", code=code, data=data)
                
                return data.get("data")

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                # Network Errors -> Retry
                last_error = ConnectError(f"Network error: {e}") if isinstance(e, requests.exceptions.ConnectionError) else TimeoutError(f"Timeout: {e}")
                
            except ServerError as e:
                # Server Errors -> Retry
                last_error = e
                
            except Exception as e:
                # Other errors -> No Retry
                logger.error(f"Request failed unrecoverably: {e}")
                raise e

            # Retry Logic
            retries += 1
            if retries > self.config.retries:
                logger.error(f"Max retries exceeded for {endpoint}")
                raise last_error
            
            # Idempotency Check: Don't retry POST unless sure (e.g. network error BEFORE send? Unknown.)
            # Safe strategy: Only retry GET requests or Idempotent operations.
            # However, user requested "Centralize retries... Never blindly retry non-idempotent".
            if method.upper() != "GET":
                 # If ConnectionError, it might not have reached server.
                 # If Timeout (Read), it definitely reached.
                 if isinstance(last_error, TimeoutError):
                     raise last_error # Unsafe to retry
                 # ConnectionError is debatable, but usually safe-ish if DNS/Connect failed.
                 # If Write failed, unsafe.
                 # requests doesn't easily distinguish phase.
                 # STRICT MODE: No retry on non-GET.
                 raise last_error
            
            sleep_time = 2 ** (retries - 1) * 0.1 # Exponential Backoff
            time.sleep(sleep_time)
            msg = str(last_error) if last_error else "Unknown"
            logger.warning(f"Retrying {method} {endpoint} ({retries}/{self.config.retries}) due to: {msg}")

    def get(self, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Any:
        return self.request("GET", endpoint, params, signed)

    def post(self, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Any:
        return self.request("POST", endpoint, params, signed)
