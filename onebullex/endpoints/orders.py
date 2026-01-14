from typing import List, Dict, Any, Optional, Union
from ..endpoints.base import BaseEndpoint
from ..models.orders import PlaceSpotOrder, OrderType, OrderSide

class Orders(BaseEndpoint):
    """Spot Order Management"""

    def place(self, order: PlaceSpotOrder) -> Dict[str, Any]:
        """
        Place a new spot order. 
        Takes a Pydantic model for validation.
        """
        # Convert Enum to int values
        params = order.model_dump()
        params['orderType'] = order.orderType.value
        params['side'] = order.side.value
        
        return self.client.post("/open/spot/order", params, signed=True)

    def cancel(self, code: int) -> Dict[str, Any]:
        """Cancel a spot order by code."""
        return self.client.post("/open/spot/order/cancel", {"code": code}, signed=True)

    def cancel_all(self, symbol: str) -> None:
        """Cancel all spot orders for a symbol."""
        self.client.post("/open/spot/order/cancel/all", {"symbol": symbol}, signed=True)

    def list(self, page: int = 1, page_size: int = 10, symbol: str = None, 
             status: int = 0) -> Dict[str, Any]:
        """Get spot orders."""
        params = {
            "page": page,
            "pageSize": page_size,
            "symbol": symbol,
            "status": status
        }
        return self.client.get("/open/spot/order/list", params, signed=True)

    def pending(self, page: int = 1, page_size: int = 10, symbol: str = None) -> Dict[str, Any]:
        """Get pending spot orders."""
        params = {
            "page": page,
            "pageSize": page_size,
            "symbol": symbol
        }
        return self.client.get("/open/spot/order/pending", params, signed=True)
