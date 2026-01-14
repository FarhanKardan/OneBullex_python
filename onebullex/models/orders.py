from enum import IntEnum
from pydantic import BaseModel, Field, field_validator

class OrderType(IntEnum):
    LIMIT = 1
    MARKET = 2

class OrderSide(IntEnum):
    BUY = 1
    SELL = 2

class MarginMode(IntEnum):
    ISOLATED = 1
    CROSS = 2

class PlaceSpotOrder(BaseModel):
    symbol: str
    side: OrderSide
    orderType: OrderType
    price: str
    quantity: str = None
    amount: str = None
    
    @field_validator('amount')
    def validate_amount_qty(cls, v, values):
        if not v and not values.data.get('quantity'):
            raise ValueError('Either quantity or amount is required')
        return v
