import os
from dotenv import load_dotenv
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from rich import print

load_dotenv()


class Icx:

    ICON_SERVICE = IconService(HTTPProvider(os.environ["CTZ_API_ENDPOINT"], 3))
    CHAIN_SCORE = "cx0000000000000000000000000000000000000000"
    GOVERNANCE_SCORE = "cx0000000000000000000000000000000000000001"

    def __init__(self) -> None:
        pass

    def call(self, to, method, params=None):
        call = CallBuilder().to(to).method(method).params(params).build()
        try:
            result = self.ICON_SERVICE.call(call)
            return result
        except Exception as e:
            print(e)

    def get_icx_usd_price(self):
        params = {"_symbol": "ICX"}
        result = self.call(
            "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132", "get_ref_data", params
        )
        icx_usd_price = int(result["rate"], 16) / 1000000000
        return icx_usd_price

    def get_iiss_info(self):
        result = self.call(self.CHAIN_SCORE, "getIISSInfo")
        for k, v in result.items():
            if isinstance(v, str):
                result[k] = int(v, 16)
        for k, v in result["rcResult"].items():
            if isinstance(v, str) and k != "stateHash":
                result["rcResult"][k] = int(v, 16)
        for k, v in result["variable"].items():
            if isinstance(v, str):
                result["variable"][k] = int(v, 16)
        return result

    def get_network_info(self):
        result = self.call(self.CHAIN_SCORE, "getNetworkInfo")
        for k, v in result.items():
            if isinstance(v, str):
                result[k] = int(v, 16)
        for k, v in result["rewardFund"].items():
            if isinstance(v, str):
                result["rewardFund"][k] = int(v, 16)
        return result

    def get_total_supply(self):
        result = self.ICON_SERVICE.get_total_supply()
        return result
