# borreguil

A lightweight, fast Python library for Ethereum JSON-RPC. Built as a minimal alternative to web3.py with low overhead and a small, explicit API.

## Install

```bash
uv add borreguil
```

## Usage

```python
from borreguil.provider import HttpProvider
from borreguil.contract import Contract

provider = HttpProvider("https://eth.llamarpc.com")

# Query chain state
block_number = provider.get_block_number()

# Call a contract
usdc = Contract(address="0xA0b...", abi=ABI, provider=provider)
response = usdc.functions.balanceOf("0x...").call()
```

## Why borreguil

- **Minimal**: No middleware stacks or heavy abstractions, just direct JSON-RPC wrappers.
- **Fast**: Low per-call overhead; uses `orjson` and `httpx` under the hood.
- **Typed**: Modern Python 3.11+ type hints throughout.
- **Small API surface**: Easy to learn and maintain.

## Documentation

See [docs/](docs/docs/intro.md) for the full guide and [examples/](examples/) for runnable snippets.
