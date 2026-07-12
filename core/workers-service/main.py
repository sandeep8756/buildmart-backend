import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from shared.models import HealthResponse, Worker
from data import WORKERS

app = FastAPI(
    title="Workers Core Service",
    description="Core microservice for skilled workers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(service="workers-service", status="healthy")


@app.get("/api/v1/workers", response_model=list[Worker])
def list_workers(
    category: str | None = Query(None),
    search: str | None = Query(None),
    available: bool | None = Query(None),
    verified: bool | None = Query(None),
):
    results = WORKERS
    if category:
        results = [w for w in results if w["category"] == category]
    if search:
        q = search.lower()
        results = [
            w for w in results
            if q in w["name"].lower()
            or q in w["location"].lower()
            or any(q in s.lower() for s in w["skills"])
        ]
    if available is not None:
        results = [w for w in results if w["available"] == available]
    if verified is not None:
        results = [w for w in results if w["verified"] == verified]
    return results


@app.get("/api/v1/workers/categories/list")
def list_categories():
    categories = sorted({w["category"] for w in WORKERS})
    return {"categories": categories, "total": len(categories)}


@app.get("/api/v1/workers/{worker_id}", response_model=Worker)
def get_worker(worker_id: str):
    for worker in WORKERS:
        if worker["id"] == worker_id:
            return worker
    raise HTTPException(status_code=404, detail="Worker not found")
