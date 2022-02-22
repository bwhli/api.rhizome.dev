from api_rhizome_dev.app.routers import icx
from api_rhizome_dev.app.utils import is_production
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

if is_production() is True:
    origins = [
        "https://icon.community",
        "https://compassionate-yonath-d3429f.netlify.app",
    ]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(icx.router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")


@app.get("/healthz/", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
async def health_check():
    return
