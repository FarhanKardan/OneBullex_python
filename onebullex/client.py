import logging
import time
from typing import Optional, Union

from .config import APIConfig, PROD_CONFIG, TEST_CONFIG
from .utils import TimeSync
from .auth.signer import Signer
from .transport.http import HTTPClient
from .endpoints.market import Market
from .endpoints.orders import Orders
from .endpoints.account import Account

class OneBullExClient:
    """
    Main OneBullEx API Client.
    Composes all endpoints and manages infrastructure.
    """

    def __init__(self, 
                 api_key: Optional[str] = None, 
                 secret: Optional[str] = None, 
                 identify: Optional[str] = None,
                 config: APIConfig = PROD_CONFIG,
                 logger_name: str = "onebullex"):
        
        self.config = config
        self.logger = logging.getLogger(logger_name)
        
        # Core Components
        self.time_sync = TimeSync() if api_key else None
        
        if api_key and secret and identify:
            self.signer = Signer(api_key, secret, identify, self.time_sync)
        else:
            self.signer = None # Public Only mode
            
        self.http = HTTPClient(config, self.signer)
        
        # Endpoints
        self.market = Market(self.http)
        self.orders = Orders(self.http)
        self.account = Account(self.http)

    def sync_time(self):
        """Manually trigger time sync via a public endpoint call."""
        # Simple strategy: Call public time or just any public endpoint and use header date?
        # OneBullEx response headers might contain time.
        # Implemented in TimeSync to be updated manually or by client hook.
        # For now, we perform a cheap public call to estimate logic if needed, 
        # or rely on client usage.
        # Let's perform a lightweight call.
        if self.time_sync:
            # We don't have a specific "time" endpoint.
            # We'll use 'timestamp' from orderbook or summary.
            data = self.market.orderbook("BTCUSDT") # Heuristic
            # If data has timestamp
            if data and 'timestamp' in data:
                 self.time_sync.update(int(data['timestamp']))
