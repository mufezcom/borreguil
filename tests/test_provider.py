"""Unit tests for borreguil/provider.py using mocked HTTP responses."""

import json
from unittest.mock import MagicMock, patch

import pytest

from borreguil.errors import DeserializationFailed, RPCError
from borreguil.provider import HttpProvider
from borreguil.types.provider import LogFilter


def _mock_response(
    status_code: int = 200,
    result: object = None,
    id_: int = 1,
    error: dict | None = None,
) -> MagicMock:
    payload: dict = {"jsonrpc": "2.0", "id": id_}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    mock = MagicMock()
    mock.status_code = status_code
    mock.content = json.dumps(payload).encode()
    return mock


@pytest.fixture
def provider():
    mock_client = MagicMock()
    with patch("borreguil.provider.httpx.Client", return_value=mock_client):
        p = HttpProvider("http://test.local", request_params={"timeout": 5})
    p._mock_post = mock_client.post
    return p


# ---------------------------------------------------------------------------
# make_request
# ---------------------------------------------------------------------------


def test_make_request_success(provider):
    provider._mock_post.return_value = _mock_response(result="0xabc", id_=1)
    resp = provider.make_request("eth_test", ["param1"])

    assert resp["result"] == "0xabc"
    assert resp["id"] == 1

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["url"] == "http://test.local"
    assert call_args.kwargs["json"]["method"] == "eth_test"
    assert call_args.kwargs["json"]["params"] == ["param1"]
    assert call_args.kwargs["json"]["jsonrpc"] == "2.0"


def test_make_request_increments_id(provider):
    provider._mock_post.return_value = _mock_response(result="0x0", id_=1)
    provider.make_request("eth_a", [])

    provider._mock_post.return_value = _mock_response(result="0x0", id_=2)
    provider.make_request("eth_b", [])

    calls = provider._mock_post.call_args_list
    assert calls[0].kwargs["json"]["id"] == 1
    assert calls[1].kwargs["json"]["id"] == 2


def test_make_request_http_error(provider):
    provider._mock_post.return_value = _mock_response(status_code=500, result=None, id_=1)
    with pytest.raises(RPCError) as exc_info:
        provider.make_request("eth_test", [])
    assert exc_info.value.code == 500
    assert "HTTP request failed" in exc_info.value.message


def test_make_request_deserialization_error(provider):
    mock = MagicMock()
    mock.status_code = 200
    mock.content = b"not valid json"
    provider._mock_post.return_value = mock

    with pytest.raises(DeserializationFailed):
        provider.make_request("eth_test", [])


def test_make_request_rpc_error(provider):
    provider._mock_post.return_value = _mock_response(
        id_=99,
        error={"code": -32601, "message": "Method not found"},
    )
    with pytest.raises(RPCError) as exc_info:
        provider.make_request("eth_invalidMethod", [])
    assert exc_info.value.code == -32601
    assert exc_info.value.message == "Method not found"
    assert exc_info.value.data is None


def test_make_request_rpc_error_with_data(provider):
    provider._mock_post.return_value = _mock_response(
        id_=99,
        error={"code": -32000, "message": "execution reverted", "data": "0x08c379a0"},
    )
    with pytest.raises(RPCError) as exc_info:
        provider.make_request("eth_call", [{}])
    assert exc_info.value.code == -32000
    assert exc_info.value.data == "0x08c379a0"


# ---------------------------------------------------------------------------
# get_block_number
# ---------------------------------------------------------------------------


def test_get_block_number(provider):
    provider._mock_post.return_value = _mock_response(result="0x17e5650", id_=1)
    block = provider.get_block_number()
    assert block == 25056848

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["method"] == "eth_blockNumber"
    assert call_args.kwargs["json"]["params"] == []


# ---------------------------------------------------------------------------
# get_transaction_count
# ---------------------------------------------------------------------------


def test_get_transaction_count_with_string_block(provider):
    provider._mock_post.return_value = _mock_response(result="0x1e1", id_=1)
    address = "0x3Ba6eB0e4327B96aDe6D4f3b578724208a590CEF"
    count = provider.get_transaction_count(address, block="latest")
    assert count == 481

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["method"] == "eth_getTransactionCount"
    assert call_args.kwargs["json"]["params"] == [address, "latest"]


def test_get_transaction_count_default_block(provider):
    provider._mock_post.return_value = _mock_response(result="0x0", id_=1)
    address = "0x3Ba6eB0e4327B96aDe6D4f3b578724208a590CEF"
    provider.get_transaction_count(address)

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["params"] == [address, "latest"]


def test_get_transaction_count_with_int_block(provider):
    provider._mock_post.return_value = _mock_response(result="0x5", id_=1)
    address = "0x3Ba6eB0e4327B96aDe6D4f3b578724208a590CEF"
    provider.get_transaction_count(address, block=25002064)

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["params"] == [address, 25002064]


# ---------------------------------------------------------------------------
# get_transaction_by_hash
# ---------------------------------------------------------------------------

TX_RESULT = {
    "blockHash": "0x84b4cea1a84eaa516945938d0add06fbffed08e52faaf58a779f5e0253c97ecc",
    "blockNumber": "0x17e5650",
    "blockTimestamp": "0x69ff0893",
    "from": "0xa0e8efdf37d641ed4c372408ba1ebb135efd6f23",
    "gas": "0x88b8",
    "gasPrice": "0x27eb5df6",
    "maxFeePerGas": "0x2ff821fb",
    "maxPriorityFeePerGas": "0x1ff34b70",
    "hash": "0x4ecd60f76989d67ef50b30e031103d30c2a7a8523fe2e1e901dc46042c9b1d53",
    "input": "0x69ff0895874b7de518005eba9fb4100005f5f6a8090000000000fafa00019e0c3980d000",
    "nonce": "0x8000",
    "to": "0x681e908b8ab57c49c74d770f369754ccc3e1ae09",
    "transactionIndex": "0x0",
    "value": "0x0",
    "type": "0x2",
    "accessList": [],
    "chainId": "0x1",
    "v": "0x0",
    "r": "0xf734f845a935118a0f943c39901da673a01318b90c7f9f0474f3e2923999c4aa",
    "s": "0x2dea09ad26ec6c21105f1351c9523534b7a5d2461b01f8bb360e30c7dd3299cd",
    "yParity": "0x0",
}


def test_get_transaction_by_hash_found(provider):
    provider._mock_post.return_value = _mock_response(result=TX_RESULT, id_=1)
    tx = provider.get_transaction_by_hash(TX_RESULT["hash"])

    assert tx is not None
    assert tx.hash == TX_RESULT["hash"]
    assert tx.from_address == TX_RESULT["from"]
    assert tx.blockNumber == TX_RESULT["blockNumber"]
    assert tx.blockHash == TX_RESULT["blockHash"]
    assert tx.value == TX_RESULT["value"]
    assert tx.gas == TX_RESULT["gas"]
    assert tx.type == TX_RESULT["type"]
    assert tx.yParity == TX_RESULT["yParity"]

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["method"] == "eth_getTransactionByHash"
    assert call_args.kwargs["json"]["params"] == [TX_RESULT["hash"]]


def test_get_transaction_by_hash_not_found(provider):
    provider._mock_post.return_value = _mock_response(result=None, id_=1)
    tx = provider.get_transaction_by_hash("0x" + "00" * 32)
    assert tx is None


# ---------------------------------------------------------------------------
# get_transaction_by_block_number_and_index
# ---------------------------------------------------------------------------


def test_get_transaction_by_block_number_and_index_found(provider):
    provider._mock_post.return_value = _mock_response(result=TX_RESULT, id_=1)
    tx = provider.get_transaction_by_block_number_and_index(0x17E5650, 0)

    assert tx is not None
    assert tx.hash == TX_RESULT["hash"]

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["method"] == "eth_getTransactionByBlockNumberAndIndex"
    assert call_args.kwargs["json"]["params"] == ["0x17e5650", "0x0"]


def test_get_transaction_by_block_number_and_index_with_string_block(provider):
    provider._mock_post.return_value = _mock_response(result=TX_RESULT, id_=1)
    provider.get_transaction_by_block_number_and_index("latest", 5)

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["params"] == ["latest", "0x5"]


def test_get_transaction_by_block_number_and_index_not_found(provider):
    provider._mock_post.return_value = _mock_response(result=None, id_=1)
    tx = provider.get_transaction_by_block_number_and_index("latest", 999)
    assert tx is None


# ---------------------------------------------------------------------------
# get_code_at
# ---------------------------------------------------------------------------

CODE_RESULT = (
    "0x60806040526004361061006d576000357c010000000000000000000000000000"
    "0000000000000000000000000000900463ffffffff1680633659cfe614610077"
)


def test_get_code_at(provider):
    provider._mock_post.return_value = _mock_response(result=CODE_RESULT, id_=1)
    result = provider.get_code_at(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        block="latest",
    )
    assert result == CODE_RESULT

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["method"] == "eth_getCode"
    assert call_args.kwargs["json"]["params"] == [
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "latest",
    ]


# ---------------------------------------------------------------------------
# get_logs
# ---------------------------------------------------------------------------

LOGS_RESULT = [
    {
        "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "topics": [
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x000000000000000000000000e0554a476a092703abdb3ef35c80e0d76d32939f",
            "0x000000000000000000000000111111125421ca6dc452d289314280a0f8842a65",
        ],
        "data": "0x000000000000000000000000000000000000000000000000000000000e12cce5",
        "blockNumber": "0x17e55f1",
        "transactionHash": "0x98e801dff97fe30d77143a064a2eadf65548be3c501ff3cff726bca3da41a7a5",
        "transactionIndex": "0x0",
        "blockHash": "0x0081349da2b07b1fe3284383de85eea7a0b7e93562c8da391caacb1d02b92deb",
        "logIndex": "0x1",
        "removed": False,
    },
    {
        "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "topics": [
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x000000000000000000000000111111125421ca6dc452d289314280a0f8842a65",
            "0x00000000000000000000000074de5d4fcbf63e00296fd95d33236b9794016631",
        ],
        "data": "0x000000000000000000000000000000000000000000000000000000000e12cce5",
        "blockNumber": "0x17e55f1",
        "transactionHash": "0x98e801dff97fe30d77143a064a2eadf65548be3c501ff3cff726bca3da41a7a5",
        "transactionIndex": "0x0",
        "blockHash": "0x0081349da2b07b1fe3284383de85eea7a0b7e93562c8da391caacb1d02b92deb",
        "logIndex": "0x4",
        "removed": False,
    },
]


def test_get_logs(provider):
    provider._mock_post.return_value = _mock_response(result=LOGS_RESULT, id_=1)
    filter_ = LogFilter(
        address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        from_block="0x17e55f1",
        to_block="0x17e55f1",
        topics=["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"],
    )
    logs = provider.get_logs(filter_)

    assert len(logs) == 2
    assert logs[0].address == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    assert logs[0].logIndex == "0x1"
    assert logs[0].topics == LOGS_RESULT[0]["topics"]
    assert logs[0].removed is False
    assert logs[1].logIndex == "0x4"

    call_args = provider._mock_post.call_args
    assert call_args.kwargs["json"]["method"] == "eth_getLogs"
    assert call_args.kwargs["json"]["params"] == [filter_.build()]
