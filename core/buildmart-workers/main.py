import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

import utils.logging_cfg
from application.api.v1 import v1
from middleware import Middle
from utils.common_api import common_v1
from utils.exceptions import Error

app = FastAPI(title="BuildMart Workers Core", version="1.0.0")

app.add_middleware(Middle)
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"service": "buildmart-workers", "host": os.environ.get("HOSTNAME", "local")}


@app.exception_handler(Error)
async def exception_handler(request: Request, exc: Error):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.error})


app.include_router(v1, prefix="/buildmart-workers")
app.include_router(common_v1, prefix="/buildmart-workers/common")
