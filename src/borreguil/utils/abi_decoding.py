import re
from collections.abc import Sequence
from typing import Any

from .abi_encoding import strip_0x

WORD_SIZE = 32


def _read_word(data: bytes, offset: int) -> bytes:
    word = data[offset : offset + WORD_SIZE]
    if len(word) != WORD_SIZE:
        raise ValueError(f"Not enough data to read ABI word at offset {offset}")
    return word


def _decode_uint_word(word: bytes) -> int:
    return int.from_bytes(word, byteorder="big", signed=False)


def _decode_int_word(word: bytes) -> int:
    return int.from_bytes(word, byteorder="big", signed=True)


def _is_dynamic_type(typ: str) -> bool:
    return typ in ("bytes", "string") or typ.endswith("[]")


def _parse_array_type(typ: str) -> str | None:
    if typ.endswith("[]"):
        return typ[:-2]
    return None


def _decode_static(typ: str, data: bytes, offset: int) -> Any:
    word = _read_word(data, offset)

    if typ == "address":
        return "0x" + word[-20:].hex()

    if typ == "bool":
        return _decode_uint_word(word) != 0

    if typ.startswith("uint"):
        return _decode_uint_word(word)

    if typ.startswith("int"):
        return _decode_int_word(word)

    fixed_bytes_match = re.fullmatch(r"bytes([1-9]|[12][0-9]|3[0-2])", typ)
    if fixed_bytes_match:
        return word[: int(fixed_bytes_match.group(1))]

    raise NotImplementedError(f"Static ABI type not supported: {typ}")


def _decode_dynamic(typ: str, data: bytes, offset: int) -> Any:
    size = _decode_uint_word(_read_word(data, offset))
    values_offset = offset + WORD_SIZE

    if typ == "bytes":
        return data[values_offset : values_offset + size]

    if typ == "string":
        return data[values_offset : values_offset + size].decode("utf-8")

    item_type = _parse_array_type(typ)
    if item_type is not None:
        if _is_dynamic_type(item_type):
            raise NotImplementedError("Nested dynamic arrays are not implemented")

        return tuple(_decode_static(item_type, data, values_offset + idx * WORD_SIZE) for idx in range(size))

    raise NotImplementedError(f"Dynamic ABI type not supported: {typ}")


def abi_decode(types: Sequence[str], data: bytes | str) -> tuple[Any, ...]:
    raw_data = bytes.fromhex(strip_0x(data)) if isinstance(data, str) else data
    head_size = len(types) * WORD_SIZE
    if len(raw_data) < head_size:
        raise ValueError("ABI data is shorter than the expected head size")

    result: list[Any] = []
    for idx, typ in enumerate(types):
        offset = idx * WORD_SIZE
        if _is_dynamic_type(typ):
            dynamic_offset = _decode_uint_word(_read_word(raw_data, offset))
            result.append(_decode_dynamic(typ, raw_data, dynamic_offset))
        else:
            result.append(_decode_static(typ, raw_data, offset))

    return tuple(result)
