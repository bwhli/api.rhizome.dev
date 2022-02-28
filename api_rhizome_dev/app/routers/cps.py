from api_rhizome_dev.app.cps import Cps
from api_rhizome_dev.app.utils import human_format
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/cps")
cps = Cps()


@router.get("/project-count/")
def get_project_count(format: str = "json", type: str = None):
    projects = cps.get_project_count()
    if format == "html":
        if type == "active":
            project_count = projects["_active"]["_count"]
        if type == "completed":
            project_count = projects["_completed"]["_count"]
        html_content = f"{project_count}"
        return HTMLResponse(content=html_content)


@router.get("/distributed-funds/")
def get_distributed_funds():
    projects = cps.get_project_count()
    completed_projects = projects["_completed"]
    distributed_funds = completed_projects["_total_amount"]
    distributed_icx = distributed_funds["ICX"]
    distributed_bnusd = distributed_funds["bnUSD"]
    distributed_funds_in_usd = (
        distributed_icx * cps.get_icx_usd_price() + distributed_bnusd
    )
    html_content = f"${distributed_funds_in_usd:,.0f}"
    return HTMLResponse(content=html_content)


@router.get("/prep-count/")
def get_prep_count():
    prep_count = cps.get_prep_count()
    html_content = f"{prep_count}"
    return HTMLResponse(content=html_content)
