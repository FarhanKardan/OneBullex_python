from typing import Dict, Any
from ..endpoints.base import BaseEndpoint

class Account(BaseEndpoint):
    """Account & Asset Management"""
    
    # Note: Spot Asset info isn't explicitly in Open API list in doc?
    # Doc 4.2 is public spot asset list.
    # Doc 5.11 is Contract Asset Info.
    # Where is Spot Private Balance?
    # The doc doesn't explicitly list `GET /open/spot/account` or `balance`.
    # It lists `/open/contract/asset`.
    # Maybe `/v1/spot/asset` is generic info, not user balance.
    # Checking doc... "5. Open API ... used for trading operations and account queries"
    # Endpoints:
    # Spot: Order, Cancel, List, Pending, History, Product List.
    # Contract: Position, Order, Product, Asset (5.11).
    # Admin: Referral.
    # It seems there is NO specific endpoint for SPOT Account Balance in the provided snippet?
    # "4.1 Get Spot Market Summary" - Public.
    # "5.11 Get Contract Asset Info" - Private.
    # Perhaps spot balance is missing from this doc version or implied?
    # I will implement what is available.
    
    def contract_assets(self) -> Dict[str, Any]:
        """Get Contract Account Asset Info"""
        return self.client.get("/open/contract/asset", signed=True)
    
    def contract_positions(self, page: int = 1, page_size: int = 10, symbol: str = None) -> Dict[str, Any]:
        """Get Contract Positions"""
        return self.client.get("/open/contract/position/list", {
            "page": page, "pageSize": page_size, "symbol": symbol
        }, signed=True)
