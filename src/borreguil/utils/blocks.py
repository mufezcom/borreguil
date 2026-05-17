from typing import Final, Literal

from ..errors import InvalidBlockProvided
from ..types.provider import BlockIdentifier

SPECIAL_BLOCKS: Final = {"latest", "earliest", "pending", "safe", "finalized"}
BLOCK_PARAMS: Final = Literal["latest", "earliest", "pending", "safe", "finalized"]


def parse_block_identifier(
    block_identifier: BlockIdentifier,
    default_block: str | int = "latest",
) -> int | str:
    """Validate the block indentifier falling back to default if it is None"""
    if block_identifier is None:
        return default_block

    if block_identifier in SPECIAL_BLOCKS:
        return block_identifier

    if isinstance(block_identifier, int):
        if block_identifier < 0:
            raise InvalidBlockProvided

        return block_identifier

    raise InvalidBlockProvided
