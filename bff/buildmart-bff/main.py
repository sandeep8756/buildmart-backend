import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

import utils.logging_cfg
from application.router import router as api_router
from middleware import Middle
from utils.common_api import common_v1
from utils.exceptions import Error

app = FastAPI(title="BuildMart BFF", version="1.0.0")
origins = ["*"]

app.add_middleware(Middle)
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {
        "service": "buildmart-bff",
        "message": "M&P – Buy Materials. Book Workers. Build Faster.",
        "core_materials": os.environ.get("ip_port_materials", "localhost:8001"),
    }


@app.exception_handler(Error)
async def exception_handler(request: Request, exc: Error):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.error})


app.include_router(api_router, prefix="/buildmart-bff")
app.include_router(common_v1, prefix="/buildmart-bff/common")
