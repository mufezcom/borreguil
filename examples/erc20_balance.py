import sys
from pathlib import Path
from typing import Final

from eth_typing.abi import ABI
from eth_utils.address import to_checksum_address

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.contract import Contract
from src.provider import HttpProvider

ETH_RPC_URL = "https://ethereum-rpc.publicnode.com"
CRV_ADDRESS = to_checksum_address("0xD533a949740bb3306d119CC777fa900bA034cd52")
ADDRESS_TO_CHECK = "0xF5d90Ac6747CB3352F05BF61f48b991ACeaE28eB"

ERC20: Final[ABI] = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]


def main():
    provider = HttpProvider(ETH_RPC_URL, request_params={"timeout": 3})
    usdc = Contract(address=CRV_ADDRESS, abi=ERC20, provider=provider)

    print(provider.get_block_number())
    response = usdc.functions.balanceOf(ADDRESS_TO_CHECK).call()
    print(response)

    if "result" in response:
        raw_balance = int(response["result"], 16)
        usdc_balance = raw_balance / 10**18
        print(f"CRV balance: {usdc_balance}")


if __name__ == "__main__":
    main()
