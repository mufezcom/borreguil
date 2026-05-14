---
slug: /
---

# Introduction

**web3o** is a lightweight, modern Python client for interacting with Ethereum nodes via JSON-RPC. It provides a simple, intuitive API for making RPC calls, querying blockchain data, and interacting with smart contracts.

## Features

- **Simple HTTP Provider** – Make JSON-RPC calls to any Ethereum node
- **Contract Interaction** – Call smart contract functions with ABI encoding
- **Type Safety** – Strongly typed data structures for transactions, logs, and blocks
- **Zero Bloat** – Minimal dependencies, fast execution

## Example

```python
from src.provider import HttpProvider

provider = HttpProvider(
    uri="https://eth.llamarpc.com",
    request_params={"timeout": 30}
)

block_number = provider.get_block_number()
print(f"Latest block: {block_number}")
```
