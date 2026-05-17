# Installation

borreguil uses `uv` for Python dependency management.

## Requirements

- Python >= 3.11

## Install Dependencies

```bash
uv sync
```

This will install all required packages including:

| Package | Purpose |
|---------|---------|
| `httpx` | HTTP client for RPC requests |
| `orjson` | Fast JSON serialization |
| `eth-utils` | Ethereum utility functions |
| `eth-typing` | Ethereum type definitions |
| `pycryptodome` | Cryptographic hashing (Keccak-256) |

## Development Dependencies

```bash
uv sync --dev
```

Additional dev tools:

| Package | Purpose |
|---------|---------|
| `ruff` | Linting and formatting |
| `ty` | Type checking |
