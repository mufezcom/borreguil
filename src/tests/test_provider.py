from src.provider import HttpProvider


def test_request():
    provider = HttpProvider("https://rpc.eth.gateway.fm", request_params={"timeout": 5})
    print(
        provider.make_request(
            method="eth_getBalance",
            params=["0x3Ba6eB0e4327B96aDe6D4f3b578724208a590CEF", "latest"],
        )
    )


test_request()
