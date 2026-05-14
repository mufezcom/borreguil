# Errors

Exception hierarchy used throughout web3o.

---

## `Web3oError`

```python
from src.errors import Web3oError
```

Base exception for all web3o errors.

---

## `InvalidBlockProvided`

```python
from src.errors import InvalidBlockProvided
```

Raised when a block identifier is invalid (e.g. negative number or unknown string).

---

## `DeserializationFailed`

```python
from src.errors import DeserializationFailed
```

Raised when an RPC response cannot be parsed as JSON.

---

## `RPCError`

```python
from src.errors import RPCError
```

Raised when the RPC node returns an error or the HTTP request fails.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `code` | `int` | Error code |
| `message` | `str` | Error message |
| `data` | `str \| None` | Optional extra data |

### String Representation

```
[code] message - data
```
