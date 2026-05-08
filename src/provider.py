from typing import Any, Literal, NotRequired, TypedDict

import httpx
import orjson

RPCId = int | str | None


class RPCError(TypedDict):
    code: int
    message: str
    data: NotRequired[str]


class RPCRequest(TypedDict):
    id: int
    jsonrpc: Literal["2.0"]
    method: str
    params: list


class RPCResponse(TypedDict, total=False):
    error: RPCError
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
        """Sends the JSON-RPC request and returns the deserialized response"""
        response = self.client.post(url=self.uri, json=self._encode_request(method, params))
        return orjson.loads(response.content)

    def get_block_number(self) -> int:
        response = self.make_request(
            method='eth_blockNumber',
            params=None,
        )
        return int(response['result'], base=16)