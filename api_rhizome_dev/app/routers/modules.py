from api_rhizome_dev import templates
from api_rhizome_dev.app.icx import Icx
from api_rhizome_dev.app.utils import human_format
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/modules")


@router.get("/validators/", status_code=status.HTTP_200_OK)
def get_validators_module(request: Request):
    _icx = Icx()
    validators = _icx.get_prep_info()
    return templates.TemplateResponse(
        "modules/validators.html",
        {
            "request": request,
            "validators": validators,
        },
    )
