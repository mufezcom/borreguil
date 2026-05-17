# Contract

The contract module lets you interact with Ethereum smart contracts using an ABI.

---

## `Contract`

```python
from borreguil.contract import Contract
```

### Constructor

```python
Contract(
    address: ChecksumAddress,
    abi: ABI,
    provider: HttpProvider
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `address` | `ChecksumAddress` | Deployed contract address |
| `abi` | `ABI` | Contract ABI (list of JSON objects) |
| `provider` | `HttpProvider` | Provider instance for RPC calls |

### `functions`

A `ContractFunctions` object exposing every function defined in the ABI as an attribute.

```python
contract.functions.balanceOf("0x...")
```

---

## `ContractFunctions`

Dynamically maps ABI function entries to `ContractMethod` instances.

Functions are sorted by name and increasing argument count (matching `web3.py` behavior).

---

## `ContractMethod`

Represents a single callable function on a contract.

### `__call__`

Accepts function arguments and returns a `ContractTransactionBuilder`.

```python
method = contract.functions.balanceOf
builder = method("0x...")
```

---

## `ContractTransactionBuilder`

Builds and sends `eth_call` transactions for read-only contract methods.

### `block`

Sets the block context for the call.

```python
builder.block(1_800_000)
```

### `call`

Encodes the function call and sends it via `eth_call`.

```python
result = builder.call()
```

The call ABI-encodes arguments using `encode_function_call`, sends the transaction object to the node, and returns the raw RPC result.
