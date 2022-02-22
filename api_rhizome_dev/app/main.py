from api_rhizome_dev.app.routers import icx
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://icon.community",
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


@app.get("/healthz/", status_code=status.HTTP_204_NO_CONTENT)
async def health_check():
    return
