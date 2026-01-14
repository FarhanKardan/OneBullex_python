from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class RestResponse(BaseModel, Generic[T]):
    code: int
    msg: str
    data: Optional[T] = None

class EmptyData(BaseModel):
    pass
