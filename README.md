# OneBullEx Python Client

[![PyPI version](https://badge.fury.io/py/onebullex.svg)](https://badge.fury.io/py/onebullex)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A production-ready, strictly typed, and robust Python client for the [OneBullEx Exchange](https://www.onebullex.com) API.

Designed for high-reliability trading systems and quantitative infrastructure.

## 🚀 Features

- **Production Grade**: Implements connection pooling, exponential backoff retries, and strict timeouts.
- **Type Safety**: Uses **Pydantic** models for requests and responses, ensuring data validity at runtime.
- **Safety First**: Proactive Client-side **Rate Limiting** (Token Bucket) and Idempotent-aware logic (no unsafe retries).
- **Clean Architecture**: Strict separation of Transport, Auth, Models, and Business Logic.
- **Developer Experience**: comprehensive type hints and IDE-friendly structure.

## 📦 Installation

Install directly from PyPI:

```bash
pip install onebullex
```

## 🛠 Usage

### Initialization

The client defaults to the **Production** environment.

```python
from onebullex import OneBullExClient

# Public only
client = OneBullExClient()

# Authenticated
client = OneBullExClient(
    api_key="YOUR_API_KEY",
    secret="YOUR_SECRET",
    identify="YOUR_IDENTIFY_CODE" # e.g. User ID or special identifier
)
```

### Market Data (Public)

```python
# Get Market Summary
summary = client.market.summary()
print(f"Active Pairs: {len(summary)}")

# Get Orderbook
depth = client.market.orderbook("BTCUSDT")
print(f"Best Bid: {depth['bids'][0]}")

# Get Candles (Klines)
candles = client.market.klines("BTCUSDT", period="1m")
```

### Trading (Authenticated)

We use Pydantic models to ensure you never send invalid order parameters.

```python
from onebullex.models.orders import PlaceSpotOrder, OrderSide, OrderType

order_params = PlaceSpotOrder(
    symbol="BTCUSDT",
    side=OrderSide.BUY,
    orderType=OrderType.LIMIT,
    price="45000.0",
    quantity="0.001"
)

try:
    response = client.orders.place(order_params)
    print(f"Order Placed ID: {response.data['orderId']}")
except Exception as e:
    print(f"Order Failed: {e}")
```

### Error Handling

The library maps exchange errors to specific Python exceptions:

```python
from onebullex.errors import InsufficientBalanceError, RateLimitError

try:
    client.orders.place(...)
except InsufficientBalanceError:
    print("Not enough funds!")
except RateLimitError:
    print("Slow down!")
```

## 🏗 Architecture

This library treats infrastructure as code:

- **`transport`**: Low-level HTTP handling with `requests.Session`, retries, and error interception.
- **`auth`**: `Signer` class implementing HMAC-SHA256 with automatic server-time drift correction.
- **`rate_limit`**: Thread-safe Token Bucket implementation.
- **`models`**: Request/Response schemas.

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
