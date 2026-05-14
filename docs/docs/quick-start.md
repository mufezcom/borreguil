# Quick Start

## Connect to a Provider

```python
from src.provider import HttpProvider

provider = HttpProvider(
    uri="https://eth.llamarpc.com",
    request_params={"timeout": 30}
)
```

## Query Blockchain Data

```python
# Get the latest block number
block_number = provider.get_block_number()

# Get transaction count for an address
nonce = provider.get_transaction_count(
    address="0x...",
    block="latest"
)

# Fetch a transaction by hash
tx = provider.get_transaction_by_hash("0x...")
```

## Interact with a Contract

```python
from src.contract import Contract

contract = Contract(
    address="0x...",
    abi=[...],  # Contract ABI
    provider=provider
)

# Call a read-only function
result = contract.functions.balanceOf("0x...").call()
```

## Filter Logs

```python
from src.types.provider import LogFilter

filter = LogFilter(
    address="0x...",
    from_block=1000000,
    to_block="latest",
    topics=["0x..."]
)

logs = provider.get_logs(filter)
```
