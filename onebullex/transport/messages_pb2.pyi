from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BaseMessage(_message.Message):
    __slots__ = ("action", "data", "time")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    action: int
    data: bytes
    time: int
    def __init__(self, action: _Optional[int] = ..., data: _Optional[bytes] = ..., time: _Optional[int] = ...) -> None: ...

class SendSubscribeInfo(_message.Message):
    __slots__ = ("symbol", "platform", "period")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    platform: str
    period: str
    def __init__(self, symbol: _Optional[str] = ..., platform: _Optional[str] = ..., period: _Optional[str] = ...) -> None: ...

class SendSubscribeDepth(_message.Message):
    __slots__ = ("symbol", "platform")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    platform: str
    def __init__(self, symbol: _Optional[str] = ..., platform: _Optional[str] = ...) -> None: ...

class SendSubscribeTicker(_message.Message):
    __slots__ = ("platform",)
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    platform: str
    def __init__(self, platform: _Optional[str] = ...) -> None: ...

class KlineInfo(_message.Message):
    __slots__ = ("open", "close", "high", "low", "volume", "startTime", "endTime")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    open: float
    close: float
    high: float
    low: float
    volume: float
    startTime: int
    endTime: int
    def __init__(self, open: _Optional[float] = ..., close: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., volume: _Optional[float] = ..., startTime: _Optional[int] = ..., endTime: _Optional[int] = ...) -> None: ...

class RecKlineData(_message.Message):
    __slots__ = ("time", "kline_infos")
    TIME_FIELD_NUMBER: _ClassVar[int]
    KLINE_INFOS_FIELD_NUMBER: _ClassVar[int]
    time: int
    kline_infos: _containers.RepeatedCompositeFieldContainer[KlineInfo]
    def __init__(self, time: _Optional[int] = ..., kline_infos: _Optional[_Iterable[_Union[KlineInfo, _Mapping]]] = ...) -> None: ...

class DepthInfo(_message.Message):
    __slots__ = ("volume", "price")
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    volume: float
    price: float
    def __init__(self, volume: _Optional[float] = ..., price: _Optional[float] = ...) -> None: ...

class RecDepthInfo(_message.Message):
    __slots__ = ("buy", "sell")
    BUY_FIELD_NUMBER: _ClassVar[int]
    SELL_FIELD_NUMBER: _ClassVar[int]
    buy: _containers.RepeatedCompositeFieldContainer[DepthInfo]
    sell: _containers.RepeatedCompositeFieldContainer[DepthInfo]
    def __init__(self, buy: _Optional[_Iterable[_Union[DepthInfo, _Mapping]]] = ..., sell: _Optional[_Iterable[_Union[DepthInfo, _Mapping]]] = ...) -> None: ...
