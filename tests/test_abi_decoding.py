from borreguil.utils.abi_decoding import abi_decode
from borreguil.utils.abi_encoding import abi_encode


def test_abi_decode_static_types():
    encoded = abi_encode(
        ["address", "uint256", "int256", "bool", "bytes4"],
        ["0x000000000000000000000000000000000000dEaD", 42, -1, True, b"\x12\x34\x56\x78"],
    )

    assert abi_decode(["address", "uint256", "int256", "bool", "bytes4"], encoded) == (
        "0x000000000000000000000000000000000000dead",
        42,
        -1,
        True,
        b"\x12\x34\x56\x78",
    )


def test_abi_decode_dynamic_types():
    encoded = abi_encode(
        ["string", "bytes", "uint256[]"],
        ["hello", b"\x12\x34", [1, 2, 3]],
    )

    assert abi_decode(["string", "bytes", "uint256[]"], encoded) == (
        "hello",
        b"\x12\x34",
        (1, 2, 3),
    )
