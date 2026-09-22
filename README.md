# Clash Controller API

Async Python client for Clash-compatible external controller APIs.

The client currently targets Clash, Clash Premium, Clash Meta, Mihomo,
clash-rs, and sing-box's Clash API compatibility layer. Endpoint capabilities
are detected at runtime because support differs between cores.

## Installation

```bash
python -m pip install clash-controller-api
```

The distribution name is `clash-controller-api`; the import name is
`clash_controller_api`. The caller owns the `aiohttp.ClientSession` passed to
`ClashAPI` and remains responsible for closing it.

## Usage

```python
import asyncio

import aiohttp
from clash_controller_api import ClashAPI


async def main():
    async with aiohttp.ClientSession() as session:
        api = ClashAPI("http://localhost:9090", "your-token", session=session)
        await api.async_validate_connection()
        result = await api.async_fetch_data()
        print(result.data)
        print(result.errors)


asyncio.run(main())
```

`async_fetch_data()` detects and caches endpoint capabilities automatically. Its
`FetchResult` contains successful responses in `data` and per-endpoint exceptions
in `errors`. Direct requests raise `APIAuthError`, `APIConnectionError` (including
`APITimeoutError`), or `APIClientError` for invalid responses. All inherit from
`ClashAPIError`.

The client does not retry requests. Polling may fall back between supported
WebSocket and HTTP transports; authentication failures stop that fallback.

## Development

Python 3.11 or newer is required.

```bash
python -m pip install -e ".[test]"
pytest
```

Run the pinned real-core contract against all supported cores with:

```bash
python tests/run.py system
```
