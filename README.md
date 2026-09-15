# Clash Controller API

Async Python client for Clash-compatible external controller APIs.

The client currently targets Clash, Clash Premium, Clash Meta, Mihomo,
clash-rs, and sing-box's Clash API compatibility layer. Endpoint capabilities
are detected at runtime because support differs between cores.

## Status

This package is under development and has not been published to PyPI yet.
The distribution name is `clash-controller-api`; the import name is
`clash_controller_api`.

## Development

Python 3.11 or newer is required.

```bash
python -m pip install -e ".[test]"
pytest
```

The caller owns the `aiohttp.ClientSession` passed to `ClashAPI` and remains
responsible for closing it.
