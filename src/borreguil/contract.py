from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from eth_typing.abi import ABI, ABIFunction
from eth_typing.evm import ChecksumAddress
from eth_utils.abi import (
    abi_to_signature,
)

from .provider import HttpProvider
from .utils.abi_encoding import encode_function_call
from .utils.blocks import parse_block_identifier

if TYPE_CHECKING:
    from .types.provider import BlockIdentifier


class ContractTransactionBuilder:
    def __init__(self, method: "ContractMethod", params: Any, provider: HttpProvider):
        self.method = method
        self.params = params
        self.provider = provider
        self._block: BlockIdentifier = None

    def block(self, block: int | str):
        self._block = block
        return self

    def call(self):
        arg_types = [input_["type"] for input_ in self.method.abi.get("inputs", [])]
        calldata = encode_function_call(
            signature=self.method.signature,
            arg_types=arg_types,
            args=self.params,
        )
        transaction = {
            "to": self.method.address,
            "data": calldata,
        }
        block = parse_block_identifier(self._block, default_block="latest")
        return self.provider.make_request(
            method="eth_call",
            params=[transaction, block],
        )


@dataclass
class ContractMethod:
    signature: str
    abi: ABIFunction
    provider: HttpProvider
    address: ChecksumAddress

    def __call__(self, *args):
        return ContractTransactionBuilder(
            method=self,
            params=args,
            provider=self.provider,
        )


class ContractFunctions:
    def __init__(self, abi: ABI, provider: HttpProvider, address: ChecksumAddress):
        self.functions: dict[str, ContractMethod] = {}
        self.abi = abi
        self.provider = provider
        self.address = address

        # mimic web3.py behaviour and sort by increasing number of arguments
        functions_abi = sorted(
            [fabi for fabi in self.abi if fabi["type"] == "function"],
            key=lambda fn: (fn["name"], len(fn.get("inputs", []))),
        )
        for func_abi in functions_abi:
            signature = abi_to_signature(func_abi)
            self.functions[func_abi["name"]] = ContractMethod(
                signature=signature,
                abi=func_abi,
                provider=self.provider,
                address=self.address,
            )

    def __getattribute__(self, name: str) -> ContractMethod:
        functions = object.__getattribute__(self, "__dict__").get("functions")
        if functions is not None and (method := functions.get(name)) is not None:
            return method

        return super().__getattribute__(name)


class Contract:
    def __init__(
        self,
        address: ChecksumAddress,
        abi: ABI,
        provider: HttpProvider,
    ):
        self.address = address
        self.abi = abi
        self.provider = provider

        self.functions = ContractFunctions(
            abi=self.abi,
            provider=self.provider,
            address=self.address,
        )
