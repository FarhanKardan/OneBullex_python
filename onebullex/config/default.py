from dataclasses import dataclass

@dataclass(frozen=True)
class APIConfig:
    """Configuration for API endpoints and behaviors."""
    rest_url: str
    ws_url: str
    timeout_connect: float = 3.05
    timeout_read: float = 10.0
    retries: int = 3
    # Weight for rate limiting (requests per second approx)
    rps: int = 10 

TEST_CONFIG = APIConfig(
    rest_url="https://bullapitest.1bullex.com/api",
    ws_url="wss://bullapitest.1bullex.com/ws/kline",
    rps=20
)

PROD_CONFIG = APIConfig(
    rest_url="https://bullapiprod.onebullex.com/api",
    ws_url="wss://bullapiprod.onebullex.com/ws/kline",
    rps=10
)
