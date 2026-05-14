from typing import Any, Literal, TypedDict

import httpx
import orjson
from eth_typing.evm import ChecksumAddress

from src.errors import DeserializationFailed, RPCError
from src.types.provider import BlockIdentifier, LogEntry, LogFilter, Transaction
from src.utils.blocks import parse_block_identifier

RPCId = int | str | None


class RPCRequest(TypedDict):
    id: int
    jsonrpc: Literal["2.0"]
    method: str
    params: list


class RPCResponse(TypedDict):
    id: RPCId
    jsonrpc: Literal["2.0"]
    result: Any


class HttpProvider:
    def __init__(
        self,
        uri: str,
        request_params: dict[str, Any],
    ):
        self.uri = uri
        self.request_params = request_params
        # default timeout in httpx is after 5 seconds of inactiviy
        self.client = httpx.Client(**self.request_params)
        self.request_counter = 1

    def _encode_request(self, method: str, params: list | None) -> RPCRequest:
        """Prepare the json payload that is sent to the RPC node"""
        request = RPCRequest(
            id=self.request_counter,
            jsonrpc="2.0",
            method=method,
            params=[] if params is None else params,
        )
        self.request_counter += 1
        return request

    def make_request(self, method: str, params: list | None) -> RPCResponse:
        """Sends the JSON-RPC request and returns the deserialized response.

        Raises:
            RPCError: If the HTTP request fails or the JSON-RPC response contains
                      an error field.
            DeserializationFailed: If JSON response is malformed
        """
        response = self.client.post(url=self.uri, json=self._encode_request(method, params))
        if response.status_code != 200:
            raise RPCError(
                code=response.status_code,
                message=f"HTTP request failed with status {response.status_code}",
            )

        try:
            payload = orjson.loads(response.content)
        except orjson.JSONDecodeError as e:
            raise DeserializationFailed(
                f"Failed to deserialize RPC response {response.content}"
            ) from e

        if "error" in payload:
            err = payload["error"]
            raise RPCError(
                code=err["code"],
                message=err["message"],
                data=err.get("data"),
            )
        return payload

    def get_block_number(self) -> int:
        response = self.make_request(
            method='eth_blockNumber',
            params=None,
        )
        return int(response['result'], base=16)

    def get_transaction_count(
        self,
        address: ChecksumAddress,
        block: BlockIdentifier = None,
    ) -> int:
        """Return the account nonce at the given block."""
        response = self.make_request(
            method="eth_getTransactionCount",
            params=[address, parse_block_identifier(block)],
        )
        return int(response["result"], base=16)

    def get_transaction_by_hash(self, transaction_hash: str) -> Transaction | None:
        response = self.make_request(
            method="eth_getTransactionByHash",
            params=[transaction_hash],
        )
        if response["result"] is None:
            return None

        return Transaction.from_rpc(response["result"])

    def get_transaction_by_block_number_and_index(
        self,
        block: BlockIdentifier,
        index: int,
    ) -> Transaction | None:
        parsed_block = parse_block_identifier(block)
        response = self.make_request(
            method="eth_getTransactionByBlockNumberAndIndex",
            params=[hex(parsed_block) if isinstance(parsed_block, int) else parsed_block, hex(index)],
        )
        if response["result"] is None:
            return None

        return Transaction.from_rpc(response["result"])

    def get_code_at(
        self,
        address: ChecksumAddress,
        block: BlockIdentifier,
    ) -> str | None:
        return self.make_request(
            method="eth_getCode",
            params=[address, parse_block_identifier(block)],
        )["result"]

    def get_logs(self, filter: LogFilter) -> list[LogEntry]:
        response = self.make_request(
            method="eth_getLogs",
            params=[filter.build()],
        )
        return [LogEntry(**log) for log in response["result"]]
