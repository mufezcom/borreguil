from dataclasses import dataclass
from typing import Any

from eth_typing import ChecksumAddress

BlockIdentifier = str | int | None
"""Represents a block identifier in the EVM chain."""


@dataclass
class Transaction:
    """An Ethereum transaction object as returned by transaction RPC methods."""

    blockHash: str | None
    blockNumber: str | None
    from_address: ChecksumAddress
    gas: str
    gasPrice: str | None
    hash: str
    input: str
    nonce: str
    to: ChecksumAddress | None
    transactionIndex: str | None
    value: str
    type: str | None = None
    chainId: str | None = None
    v: str | None = None
    r: str | None = None
    s: str | None = None
    maxFeePerGas: str | None = None
    maxPriorityFeePerGas: str | None = None
    accessList: list[dict[str, Any]] | None = None
    yParity: str | None = None

    @classmethod
    def from_rpc(cls, transaction: dict[str, Any]) -> "Transaction":
        return cls(
            blockHash=transaction.get("blockHash"),
            blockNumber=transaction.get("blockNumber"),
            from_address=transaction["from"],
            gas=transaction["gas"],
            gasPrice=transaction.get("gasPrice"),
            hash=transaction["hash"],
            input=transaction["input"],
            nonce=transaction["nonce"],
            to=transaction.get("to"),
            transactionIndex=transaction.get("transactionIndex"),
            value=transaction["value"],
            type=transaction.get("type"),
            chainId=transaction.get("chainId"),
            v=transaction.get("v"),
            r=transaction.get("r"),
            s=transaction.get("s"),
            maxFeePerGas=transaction.get("maxFeePerGas"),
            maxPriorityFeePerGas=transaction.get("maxPriorityFeePerGas"),
            accessList=transaction.get("accessList"),
            yParity=transaction.get("yParity"),
        )


@dataclass
class LogEntry:
    """An Ethereum log object as returned by eth_getLogs."""

    address: ChecksumAddress
    # Address from which this log originated.
    topics: list[str]
    # Array of zero to four 32-bytes DATA of indexed log arguments.
    data: str
    # One or more 32-bytes non-indexed arguments of the log.
    blockNumber: str | None
    # Block number (hex). null when it's a pending log.
    transactionHash: str | None
    # Transaction hash (hex). null when it's a pending log.
    transactionIndex: str | None
    # Transaction index position (hex). null when it's a pending log.
    blockHash: str | None
    # Block hash (hex). null when it's a pending log.
    logIndex: str | None
    # Log index position in the block (hex). null when it's a pending log.
    removed: bool
    # True when the log was removed due to a chain reorganization.


class LogFilter:

    def __init__(
        self,
        address: ChecksumAddress,
        from_block: BlockIdentifier = None,
        to_block: BlockIdentifier = None,
        block_hash: str | None = None,
        topics: list[str] | None = None,
    ):
        if block_hash is not None and (from_block or to_block):
            raise Exception

        self.from_block = from_block
        self.to_block = to_block
        self.address = address
        self.block_hash = block_hash
        self.topics = topics

    def build(self) -> dict[str, Any]:
        data: dict[str, Any] = {'address': self.address}
        if self.topics is not None:
            data["topics"] = self.topics
        if self.block_hash is not None:
            data["blockHash"] = self.block_hash
        if self.from_block is not None:
            data["fromBlock"] = self.from_block
        if self.to_block is not None:
            data["toBlock"] = self.to_block

        return data
