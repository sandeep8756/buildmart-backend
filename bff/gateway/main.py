import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

MATERIALS_BFF_URL = os.getenv("MATERIALS_BFF_URL", "http://localhost:8101")
WORKERS_BFF_URL = os.getenv("WORKERS_BFF_URL", "http://localhost:8102")
DELIVERY_BFF_URL = os.getenv("DELIVERY_BFF_URL", "http://localhost:8103")

app = FastAPI(
    title="M&P API Gateway",
    description="BFF Gateway - single entry point for M&P frontend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICE_MAP = {
    "materials": MATERIALS_BFF_URL,
    "workers": WORKERS_BFF_URL,
    "delivery": DELIVERY_BFF_URL,
}


@app.get("/")
def root():
    return {
        "name": "M&P API Gateway",
        "tagline": "Buy Materials. Book Workers. Build Faster.",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    statuses = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in SERVICE_MAP.items():
            try:
                response = await client.get(f"{url}/health")
                statuses[name] = response.json() if response.status_code == 200 else {"status": "unhealthy"}
            except httpx.RequestError:
                statuses[name] = {"status": "unreachable"}
    all_healthy = all(s.get("status") == "healthy" for s in statuses.values())
    return {
        "service": "api-gateway",
        "status": "healthy" if all_healthy else "degraded",
        "bffServices": statuses,
    }


@app.api_route("/api/v1/materials/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/v1/materials", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_materials(request: Request, path: str = ""):
    return await _proxy(request, MATERIALS_BFF_URL, "materials", path)


@app.api_route("/api/v1/workers/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/v1/workers", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_workers(request: Request, path: str = ""):
    return await _proxy(request, WORKERS_BFF_URL, "workers", path)


@app.api_route("/api/v1/delivery/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/v1/delivery", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_delivery(request: Request, path: str = ""):
    return await _proxy(request, DELIVERY_BFF_URL, "delivery", path)


async def _proxy(request: Request, base_url: str, resource: str, path: str):
    target_path = f"/api/v1/{resource}/{path}".rstrip("/") if path else f"/api/v1/{resource}"
    url = f"{base_url}{target_path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"
    body = await request.body()
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                content=body if body else None,
                headers={"content-type": request.headers.get("content-type", "application/json")},
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"BFF service unavailable: {exc}") from exc
    return JSONResponse(content=response.json(), status_code=response.status_code)
