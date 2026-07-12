import os

from fastapi import APIRouter

common_v1 = APIRouter(tags=["Common Diagnostics"])


@common_v1.get("/health")
async def common_health():
    return {"service": "buildmart-core-common", "status": "healthy"}


@common_v1.get("/env")
async def download_env_vars():
    return {"context_path": os.environ.get("context_path", "")}
