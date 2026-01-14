from typing import List, Dict, Any, Optional
from ..endpoints.base import BaseEndpoint

class Market(BaseEndpoint):
    """Public Market Data Endpoints"""
    
    def summary(self) -> Dict[str, Any]:
        """Get Spot Market Summary"""
        return self.client.get("/v1/spot/summary")
    
    def assets(self) -> Dict[str, Any]:
        """Get Supported Assets"""
        return self.client.get("/v1/spot/asset")

    def ticker(self) -> Dict[str, Any]:
        """Get Spot Tickers"""
        return self.client.get("/v1/spot/ticker")
    
    def orderbook(self, symbol: str) -> Dict[str, Any]:
        """Get Spot Order Book"""
        return self.client.get("/v1/spot/orderbook", {"symbol": symbol})

    def trades(self, symbol: str) -> Dict[str, Any]:
        """Get Recent Trades"""
        return self.client.get("/v1/spot/trades", {"symbol": symbol})

    def klines(self, symbol: str, period: str) -> Dict[str, Any]:
        """Get Kline Data"""
        return self.client.get("/product/history/kline", {"symbol": symbol, "period": period})
        
    def contract_list(self) -> Dict[str, Any]:
        return self.client.get("/v1/derivative/conrtacts")
        
    def contract_specs(self) -> Dict[str, Any]:
        return self.client.get("/v1/derivative/conrtact/specs")
