import os

import requests
from api_rhizome_dev.app.utils import hex_to_int
from dotenv import load_dotenv
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from rich import print

load_dotenv()


class Icx:

    ICON_SERVICE = IconService(HTTPProvider(os.getenv("CTZ_API_ENDPOINT"), 3))
    CHAIN_CONTRACT = "cx0000000000000000000000000000000000000000"
    GOVERNANCE_CONTRACT = "cx0000000000000000000000000000000000000001"
    TRACKER_API_URL = "https://tracker.icon.community/api/v1"

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
        result = self.call(self.CHAIN_CONTRACT, "getIISSInfo")
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
        result = self.call(self.CHAIN_CONTRACT, "getNetworkInfo")
        for k, v in result.items():
            if isinstance(v, str):
                result[k] = int(v, 16)
        for k, v in result["rewardFund"].items():
            if isinstance(v, str):
                result["rewardFund"][k] = int(v, 16)
        return result

    def get_prep_info(self):
        result = self.call(self.CHAIN_CONTRACT, "getPReps", {})
        preps = result["preps"]
        prep_info = []
        for prep in preps:
            if "ICONLEO" in prep["name"]:
                prep_name = "ICONLEO"
            elif "ICXburner" in prep["name"]:
                prep_name = "ICXburners"
            elif "Gilga Capital" in prep["name"]:
                prep_name = "Gilga Capital"
            elif "UNBLOCK" in prep["name"]:
                prep_name = "UNBLOCK"
            else:
                prep_name = prep["name"]

            data = {
                "name": prep_name,
                "address": prep["address"],
                "bonded": hex_to_int(prep["bonded"]),
                "delegated": hex_to_int(prep["delegated"]),
                "bond_ratio": hex_to_int(prep["bonded"])
                / hex_to_int(prep["delegated"]),
                "bonded_delegation": min(
                    hex_to_int(prep["bonded"]) * 20,
                    hex_to_int(prep["bonded"]) + hex_to_int(prep["delegated"]),
                ),
            }
            prep_info.append(data)

        total_bonded_delegation = sum(prep["bonded_delegation"] for prep in prep_info)

        for prep in prep_info:
            prep["monthly_reward"] = (
                prep["bonded_delegation"] / total_bonded_delegation
            ) * 390000
            prep["daily_reward"] = (prep["monthly_reward"] * 12) / 365

        return sorted(prep_info, key=lambda k: k["bonded_delegation"], reverse=True)

    async def get_supply(self):
        url = f"{self.TRACKER_API_URL}/metrics/supply"
        r = requests.get(url)
        return r.json()
