import re
from collections.abc import Sequence
from typing import Any

from src.utils.crypto import keccak256

HEX_RE = re.compile(r"^0x[0-9a-fA-F]*$")


def strip_0x(value: str) -> str:
    return value[2:] if value.startswith("0x") else value


def pad32(data: bytes) -> bytes:
    padding = (32 - len(data) % 32) % 32
    return data + b"\x00" * padding


def uint256(value: int) -> bytes:
    if value < 0:
        raise ValueError("uint cannot be negative")
    return value.to_bytes(32, byteorder="big")


def int256(value: int) -> bytes:
    return value.to_bytes(32, byteorder="big", signed=True)


def encode_bool(value: bool) -> bytes:
    return uint256(1 if value else 0)


def encode_address(value: str) -> bytes:
    raw = strip_0x(value)

    if len(raw) != 40:
        raise ValueError(f"Invalid address length: {value}")

    return bytes.fromhex(raw).rjust(32, b"\x00")


def encode_fixed_bytes(value: bytes | str, size: int) -> bytes:
    raw = bytes.fromhex(strip_0x(value)) if isinstance(value, str) else value

    if len(raw) != size:
        raise ValueError(f"Expected bytes{size}, got {len(raw)} bytes")

    return raw.ljust(32, b"\x00")


def encode_dynamic_bytes(value: bytes | str) -> bytes:
    raw = bytes.fromhex(strip_0x(value)) if isinstance(value, str) else value

    return uint256(len(raw)) + pad32(raw)


def encode_string(value: str) -> bytes:
    raw = value.encode("utf-8")
    return uint256(len(raw)) + pad32(raw)


def is_dynamic_type(typ: str) -> bool:
    if typ in ("bytes", "string"):
        return True

    return bool(typ.endswith("[]"))


def parse_array_type(typ: str) -> str | None:
    if typ.endswith("[]"):
        return typ[:-2]
    return None


def encode_single_static(typ: str, value: Any) -> bytes:
    if typ == "address":
        return encode_address(value)

    if typ == "bool":
        return encode_bool(value)

    if typ.startswith("uint"):
        return uint256(int(value))

    if typ.startswith("int"):
        return int256(int(value))

    fixed_bytes_match = re.fullmatch(r"bytes([1-9]|[12][0-9]|3[0-2])", typ)
    if fixed_bytes_match:
        size = int(fixed_bytes_match.group(1))
        return encode_fixed_bytes(value, size)

    raise NotImplementedError(f"Static ABI type not supported: {typ}")


def encode_single_dynamic(typ: str, value: Any) -> bytes:
    if typ == "bytes":
        return encode_dynamic_bytes(value)

    if typ == "string":
        return encode_string(value)

    item_type = parse_array_type(typ)
    if item_type is not None:
        if is_dynamic_type(item_type):
            raise NotImplementedError("Nested dynamic arrays are not implemented")

        encoded_items = b"".join(encode_single_static(item_type, item) for item in value)

        return uint256(len(value)) + encoded_items

    raise NotImplementedError(f"Dynamic ABI type not supported: {typ}")


def abi_encode(types: Sequence[str], values: Sequence[Any]) -> bytes:
    if len(types) != len(values):
        raise ValueError("types and values length mismatch")

    head_parts: list[bytes | None] = []
    tail_parts: list[bytes] = []

    for typ, value in zip(types, values, strict=True):
        if is_dynamic_type(typ):
            head_parts.append(None)
            tail_parts.append(encode_single_dynamic(typ, value))
        else:
            head_parts.append(encode_single_static(typ, value))
            tail_parts.append(b"")

    head_size = 32 * len(head_parts)

    result_head = b""
    result_tail = b""

    current_tail_offset = 0

    for head, tail in zip(head_parts, tail_parts, strict=True):
        if head is None:
            result_head += uint256(head_size + current_tail_offset)
            result_tail += tail
            current_tail_offset += len(tail)
        else:
            result_head += head

    return result_head + result_tail


def function_selector(signature: str) -> bytes:
    return keccak256(signature.encode("ascii"))[:4]


def encode_function_call(
    signature: str,
    arg_types: Sequence[str],
    args: Sequence[Any],
) -> str:
    selector = function_selector(signature)
    encoded_args = abi_encode(arg_types, args)
    return "0x" + (selector + encoded_args).hex()
