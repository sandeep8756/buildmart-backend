import os

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

CORE_URL = os.getenv("MATERIALS_CORE_URL", "http://localhost:8001")

app = FastAPI(
    title="Materials BFF",
    description="Backend-for-Frontend microservice for materials",
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
    return {"service": "materials-bff", "status": "healthy", "coreUrl": CORE_URL}


@app.get("/api/v1/materials")
async def list_materials(
    category: str | None = Query(None),
    search: str | None = Query(None),
):
    params = {}
    if category:
        params["category"] = category
    if search:
        params["search"] = search
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/materials", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
        materials = response.json()
    return {
        "data": materials,
        "total": len(materials),
        "message": "Materials fetched successfully",
    }


@app.get("/api/v1/materials/{material_id}")
async def get_material(material_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/materials/{material_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Material not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
    return {"data": response.json(), "message": "Material fetched successfully"}


@app.get("/api/v1/materials/categories/list")
async def list_categories():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/materials/categories/list")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
    return response.json()
