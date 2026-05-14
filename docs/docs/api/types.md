# Types

Core data structures for Ethereum objects.

---

## `BlockIdentifier`

```python
BlockIdentifier = str | int | None
```

A flexible block reference:
- `int` – absolute block number
- `str` – tag such as `"latest"`, `"earliest"`, `"pending"`, `"safe"`, `"finalized"`
- `None` – falls back to the default block

---

## `Transaction`

```python
from src.types.provider import Transaction
```

Dataclass representing an Ethereum transaction.

| Field | Type | Description |
|-------|------|-------------|
| `blockHash` | `str \| None` | Block hash |
| `blockNumber` | `str \| None` | Block number (hex) |
| `from_address` | `ChecksumAddress` | Sender address |
| `gas` | `str` | Gas limit |
| `gasPrice` | `str \| None` | Gas price |
| `hash` | `str` | Transaction hash |
| `input` | `str` | Call data |
| `nonce` | `str` | Transaction nonce |
| `to` | `ChecksumAddress \| None` | Recipient address |
| `transactionIndex` | `str \| None` | Index in block |
| `value` | `str` | Transferred value |
| `type` | `str \| None` | Transaction type |
| `chainId` | `str \| None` | Chain ID |
| `v` | `str \| None` | Signature v |
| `r` | `str \| None` | Signature r |
| `s` | `str \| None` | Signature s |
| `maxFeePerGas` | `str \| None` | EIP-1559 max fee |
| `maxPriorityFeePerGas` | `str \| None` | EIP-1559 priority fee |
| `accessList` | `list[dict] \| None` | Access list |
| `yParity` | `str \| None` | Y parity |

### `from_rpc`

```python
Transaction.from_rpc(transaction: dict[str, Any]) -> Transaction
```

Class method that builds a `Transaction` from a raw RPC response dict.

---

## `LogEntry`

```python
from src.types.provider import LogEntry
```

Dataclass representing an Ethereum event log.

| Field | Type | Description |
|-------|------|-------------|
| `address` | `ChecksumAddress` | Origin address |
| `topics` | `list[str]` | Indexed arguments (0–4) |
| `data` | `str` | Non-indexed arguments |
| `blockNumber` | `str \| None` | Block number (hex) |
| `transactionHash` | `str \| None` | Transaction hash |
| `transactionIndex` | `str \| None` | Transaction index |
| `blockHash` | `str \| None` | Block hash |
| `logIndex` | `str \| None` | Log index in block |
| `removed` | `bool` | Reorg flag |

---

## `LogFilter`

```python
from src.types.provider import LogFilter
```

Builds filter objects for `eth_getLogs`.

### Constructor

```python
LogFilter(
    address: ChecksumAddress,
    from_block: BlockIdentifier = None,
    to_block: BlockIdentifier = None,
    block_hash: str | None = None,
    topics: list[str] | None = None,
)
```

:::warning
`block_hash` cannot be combined with `from_block` or `to_block`.
:::

### `build`

```python
build() -> dict[str, Any]
```

Returns the JSON-RPC filter payload.
