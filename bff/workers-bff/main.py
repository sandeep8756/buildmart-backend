import os

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

CORE_URL = os.getenv("WORKERS_CORE_URL", "http://localhost:8002")

app = FastAPI(
    title="Workers BFF",
    description="Backend-for-Frontend microservice for workers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"service": "workers-bff", "status": "healthy", "coreUrl": CORE_URL}


@app.get("/api/v1/workers")
async def list_workers(
    category: str | None = Query(None),
    search: str | None = Query(None),
    available: bool | None = Query(None),
):
    params = {}
    if category:
        params["category"] = category
    if search:
        params["search"] = search
    if available is not None:
        params["available"] = available
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/workers", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
        workers = response.json()
    return {
        "data": workers,
        "total": len(workers),
        "message": "Workers fetched successfully",
    }


@app.get("/api/v1/workers/{worker_id}")
async def get_worker(worker_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/workers/{worker_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Worker not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
    return {"data": response.json(), "message": "Worker fetched successfully"}


@app.get("/api/v1/workers/categories/list")
async def list_categories():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/workers/categories/list")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
    return response.json()
