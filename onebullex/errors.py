from typing import Any, Optional

class OneBullExError(Exception):
    """Base exception for all OneBullEx client errors."""
    def __init__(self, message: str, code: Optional[int] = None, data: Optional[Any] = None):
        super().__init__(message)
        self.code = code
        self.data = data

# --- Transform Layer Errors ---

class TransportError(OneBullExError):
    """Base for transport (network) related errors."""
    pass

class ConnectError(TransportError):
    """Connection failed (timeout, DNS, etc)."""
    pass

class TimeoutError(TransportError):
    """Request timed out."""
    pass

# --- API Response Errors ---

class APIError(OneBullExError):
    """Server returned a valid response with an error code/status."""
    pass

class ClientError(APIError):
    """4xx HTTP errors or specific API error codes implying bad request."""
    pass

class ServerError(APIError):
    """5xx HTTP errors or specific API error codes implying platform issues."""
    pass

class RateLimitError(ClientError):
    """429 or specific rate limit code."""
    pass

class AuthError(ClientError):
    """Authentication failed (signatures, keys)."""
    pass

class BusinessError(APIError):
    """Logic errors (Insufficient balance, invalid order params)."""
    pass

# --- Specific Business Mapping ---
# 20008: Insufficient balance
# 20001: Invalid parameter
# 10002: Invalid signature

ERROR_CODE_MAP = {
    10001: AuthError,
    10002: AuthError,
    10003: AuthError, # Timestamp expired
    10004: AuthError, # Invalid Nonce
    10005: AuthError,
    20001: ClientError, # Invalid parameter is a Client Error
    20008: BusinessError,
    30003: RateLimitError,
}

def map_error_code(code: int, message: str, data: Any = None) -> APIError:
    """Factory to return specific exception based on error code."""
    cls = ERROR_CODE_MAP.get(code, APIError)
    if code != 0 and code != 200: # Assuming 200 is success based on verification
         return cls(f"[{code}] {message}", code=code, data=data)
    return None
