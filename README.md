# OneBullEx Python Client

A production-ready, typed, and robust Python client for the [OneBullEx Exchange](https://www.onebullex.com) API.

Designed for trading systems and quantitative infrastructure, offering:
- **Clean Architecture**: Strict separation of transport, authentication, and business logic.
- **Robustness**: Connection pooling, exponential backoff retries, and strict timeouts.
- **Type Safety**: Pydantic models for all major interactions.
- **Safety**: Proactive rate limiting and idempotent-aware retry logic.

## Installation

```bash
pip install requests pydantic
pip install -e .
```

## Quick Start

### Public Data

```python
from onebullex import OneBullExClient

# Initialize (defaults to PROD environment)
client = OneBullExClient()

# Get Market Summary
summary = client.market.summary()
print(summary)

# Get Orderbook
depth = client.market.orderbook("BTCUSDT")
print(f"Best Bid: {depth['bids'][0]}")
```

### Authenticated Trading

```python
from onebullex import OneBullExClient
from onebullex.models.orders import PlaceSpotOrder, OrderSide, OrderType

client = OneBullExClient(
    api_key="YOUR_API_KEY",
    secret="YOUR_SECRET",
    identify="YOUR_IDENTIFY_CODE"
)

# Place a Limit Order
order = PlaceSpotOrder(
    symbol="BTCUSDT",
    side=OrderSide.BUY,
    orderType=OrderType.LIMIT,
    price="45000.0",
    quantity="0.001"
)

try:
    response = client.orders.place(order)
    print(f"Order Placed: {response}")
except Exception as e:
    print(f"Trading Error: {e}")
```

## Architecture

This client treats infrastructure as code:

- **`onebullex.transport`**: Low-level HTTP/WebSocket handling with `requests.Session`.
- **`onebullex.auth`**: `Signer` class for HMAC-SHA256 signatures with automatic server-time drift correction.
- **`onebullex.models`**: Pydantic models for request validation.
- **`onebullex.errors`**: Hierarchical exception mapping (e.g., specific `InsufficientBalanceError` vs generic `ClientError`).

## Development

Run tests:
```bash
python -m unittest discover tests
```

Run verification script (Public API):
```bash
python examples/verify_rest_v2.py
```

## License

MIT
