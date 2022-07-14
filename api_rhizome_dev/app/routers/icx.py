from api_rhizome_dev.app.icx import Icx
from api_rhizome_dev.app.utils import human_format
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/icx")
icx = Icx()


@router.get("/price/")
async def get_icx_price(format: str = "json"):
    icx_usd_price = icx.get_icx_usd_price()
    if format == "html":
        html_content = f"${icx_usd_price:.2f}"
        return HTMLResponse(content=html_content)
    else:
        return {"icx_usd_price": icx_usd_price}


@router.get("/staking-apy/")
async def get_staking_apy(format: str = "json"):
    network_info = icx.get_network_info()
    reward_fund = network_info["rewardFund"]
    voter_allocation = reward_fund["Iglobal"] * (reward_fund["Ivoter"] / 100) * 12
    total_delegated = network_info["totalDelegated"]
    icx_staking_apy = voter_allocation / total_delegated
    if format == "html":
        html_content = f"{icx_staking_apy:.2%}"
        return HTMLResponse(content=html_content)
    else:
        return {"icx_staking_apy": icx_staking_apy}


@router.get("/supply/")
async def get_icx_supply(format: str = "json"):
    response = await icx.get_supply()
    total_supply = response["total_supply"] / 10**18
    if format == "html":
        html_content = f"{human_format(total_supply)}"
        return HTMLResponse(content=html_content)
    else:
        return {"icx_total_supply": total_supply}


@router.get("/market-cap/")
async def get_icx_market_cap(format: str = "json"):
    response = icx.get_supply()
    circulating_supply = float(response["tmainInfo"]["icxCirculationy"])
    icx_usd_price = icx.get_icx_usd_price()
    icx_market_cap = circulating_supply * icx_usd_price
    if format == "html":
        html_content = f"${human_format(icx_market_cap)}"
        return HTMLResponse(content=html_content)
    else:
        return {"icx_market_cap": icx_market_cap}
