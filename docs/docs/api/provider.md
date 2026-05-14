# Provider

The `HttpProvider` is the core class for communicating with an Ethereum JSON-RPC node.

---

## `HttpProvider`

```python
from src.provider import HttpProvider
```

### Constructor

```python
HttpProvider(
    uri: str,
    request_params: dict[str, Any]
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `uri` | `str` | URL of the JSON-RPC endpoint |
| `request_params` | `dict` | Extra parameters passed to `httpx.Client` |

### `make_request`

Sends a JSON-RPC request and returns the deserialized response.

```python
make_request(
    method: str,
    params: list | None
) -> RPCResponse
```

**Raises:**
- `RPCError` – if the HTTP request fails or the RPC returns an error
- `DeserializationFailed` – if the response JSON is malformed

### `get_block_number`

Returns the current latest block number as an `int`.

```python
get_block_number() -> int
```

### `get_transaction_count`

Returns the account nonce at the specified block.

```python
get_transaction_count(
    address: ChecksumAddress,
    block: BlockIdentifier = None
) -> int
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `address` | `ChecksumAddress` | Ethereum address to query |
| `block` | `BlockIdentifier` | Block number, tag, or `None` for default |

### `get_transaction_by_hash`

Fetches a transaction by its hash.

```python
get_transaction_by_hash(
    transaction_hash: str
) -> Transaction | None
```

### `get_transaction_by_block_number_and_index`

Fetches a transaction by block and index.

```python
get_transaction_by_block_number_and_index(
    block: BlockIdentifier,
    index: int
) -> Transaction | None
```

### `get_code_at`

Returns the bytecode deployed at an address.

```python
get_code_at(
    address: ChecksumAddress,
    block: BlockIdentifier
) -> str | None
```

### `get_logs`

Returns logs matching a filter.

```python
get_logs(
    filter: LogFilter
) -> list[LogEntry]
```
