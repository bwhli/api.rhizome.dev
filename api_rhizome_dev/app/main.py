from api_rhizome_dev.app.routers import icx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

origins = [
    "https://studiomirai.io",
    "http://localhost",
    "http://localhost:1313",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(icx.router, prefix="/api/v1")
