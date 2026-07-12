import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse

common_v1 = APIRouter(tags=["Common Diagnostics"])


@common_v1.get("/health")
async def common_health():
    return {"service": "buildmart-bff", "status": "healthy"}


@common_v1.get("/env")
async def download_env_vars():
    allowed = [
        "ip_port_materials",
        "ip_port_workers",
        "ip_port_delivery",
        "context_path",
    ]
    return {key: os.environ.get(key, "") for key in allowed}
