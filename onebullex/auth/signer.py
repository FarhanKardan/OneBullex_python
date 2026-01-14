import hmac
import hashlib
import uuid
from typing import Dict, Any, Tuple
from ..utils import TimeSync

class Signer:
    """Implement HMAC-SHA256 signing logic."""
    
    def __init__(self, api_key: str, secret: str, identify: str, time_sync: TimeSync):
        self.api_key = api_key
        self.secret = secret
        self.identify = identify
        self.time_sync = time_sync

    def sign(self, params: Dict[str, Any], method: str = "GET") -> Dict[str, str]:
        """
        Generates authentication headers.
        
        Algorithm:
        Content = timestamp + nonce + sorted_query_string
        Signature = HMAC_SHA256(secret, Content).upper()
        """
        timestamp = self.time_sync.get_timestamp_str()
        nonce = str(uuid.uuid4())
        
        # Filter None and convert bools
        clean_params = {}
        for k, v in params.items():
            if v is None:
                continue
            if isinstance(v, bool):
                clean_params[k] = str(v).lower()
            else:
                clean_params[k] = str(v)
                
        # Sort by key
        sorted_keys = sorted(clean_params.keys())
        query_parts = [f"{k}={clean_params[k]}" for k in sorted_keys]
        query_string = "&".join(query_parts)
        
        signature_content = f"{timestamp}{nonce}{query_string}"
        
        signature = hmac.new(
            self.secret.encode('utf-8'),
            signature_content.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
        
        return {
            "X-API-Key": self.api_key,
            "X-Signature": signature,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Identify": self.identify,
            "Identify": self.identify
        }
