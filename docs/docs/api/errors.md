# Errors

Exception hierarchy used throughout borreguil.

---

## `Web3oError`

```python
from borreguil.errors import Web3oError
```

Base exception for all borreguil errors.

---

## `InvalidBlockProvided`

```python
from borreguil.errors import InvalidBlockProvided
```

Raised when a block identifier is invalid (e.g. negative number or unknown string).

---

## `DeserializationFailed`

```python
from borreguil.errors import DeserializationFailed
```

Raised when an RPC response cannot be parsed as JSON.

---

## `RPCError`

```python
from borreguil.errors import RPCError
```

Raised when the RPC node returns an error or the HTTP request fails.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `code` | `int` | Error code |
| `message` | `str` | Error message |
| `data` | `str | None` | Optional extra data |

### String Representation

```
[code] message - data
```
