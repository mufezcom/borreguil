# Utilities

Helper modules for ABI encoding, cryptography, and block parsing.

---

## `src.utils.crypto`

### `keccak256`

```python
from borreguil.utils.crypto import keccak256

keccak256(data: bytes) -> bytes
```

Computes the Keccak-256 hash of the input bytes.

---

## `src.utils.blocks`

### `parse_block_identifier`

```python
from borreguil.utils.blocks import parse_block_identifier

parse_block_identifier(
    block_identifier: BlockIdentifier,
    default_block: str | int = "latest"
) -> int | str
```

Validates a block identifier and falls back to `default_block` when `None` is passed.

| Input | Output |
|-------|--------|
| `None` | `default_block` |
| `"latest"`, `"earliest"`, `"pending"`, `"safe"`, `"finalized"` | same string |
| positive `int` | same int |
| negative `int` or unknown string | raises `InvalidBlockProvided` |

---

## `src.utils.abi_encoding`

Full ABI encoder for Solidity function calls.

### `encode_function_call`

```python
from borreguil.utils.abi_encoding import encode_function_call

encode_function_call(
    signature: str,
    arg_types: Sequence[str],
    args: Sequence[Any]
) -> str
```

Encodes a function call into hex calldata (`0x` + selector + arguments).

### `abi_encode`

```python
from borreguil.utils.abi_encoding import abi_encode

abi_encode(
    types: Sequence[str],
    values: Sequence[Any]
) -> bytes
```

ABI-encodes a sequence of values according to their Solidity types.

Supports:
- Static types: `uint*`, `int*`, `address`, `bool`, `bytes1`–`bytes32`
- Dynamic types: `bytes`, `string`, `T[]` (single-level arrays)

### `function_selector`

```python
from borreguil.utils.abi_encoding import function_selector

function_selector(signature: str) -> bytes
```

Computes the 4-byte function selector from a signature string (e.g. `"transfer(address,uint256)"`).

### Individual Encoders

| Function | Signature | Description |
|----------|-----------|-------------|
| `strip_0x` | `(value: str) -> str` | Remove `0x` prefix |
| `pad32` | `(data: bytes) -> bytes` | Pad bytes to 32-byte boundary |
| `uint256` | `(value: int) -> bytes` | Encode unsigned 256-bit int |
| `int256` | `(value: int) -> bytes` | Encode signed 256-bit int |
| `encode_bool` | `(value: bool) -> bytes` | Encode boolean |
| `encode_address` | `(value: str) -> bytes` | Encode Ethereum address |
| `encode_fixed_bytes` | `(value: bytes | str, size: int) -> bytes` | Encode fixed `bytesN` |
| `encode_dynamic_bytes` | `(value: bytes | str) -> bytes` | Encode dynamic `bytes` |
| `encode_string` | `(value: str) -> bytes` | Encode UTF-8 string |
| `is_dynamic_type` | `(typ: str) -> bool` | Check if a type is dynamic |
| `encode_single_static` | `(typ: str, value: Any) -> bytes` | Encode a single static value |
| `encode_single_dynamic` | `(typ: str, value: Any) -> bytes` | Encode a single dynamic value |
