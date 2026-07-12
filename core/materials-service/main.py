import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from shared.models import HealthResponse, Material
from data import MATERIALS

app = FastAPI(
    title="Materials Core Service",
    description="Core microservice for construction materials",
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
    return HealthResponse(service="materials-service", status="healthy")


@app.get("/api/v1/materials", response_model=list[Material])
def list_materials(
    category: str | None = Query(None),
    search: str | None = Query(None),
    in_stock: bool | None = Query(None, alias="inStock"),
):
    results = MATERIALS
    if category:
        results = [m for m in results if m["category"] == category]
    if search:
        q = search.lower()
        results = [
            m for m in results
            if q in m["name"].lower() or q in m["brand"].lower()
        ]
    if in_stock is not None:
        results = [m for m in results if m["inStock"] == in_stock]
    return results


@app.get("/api/v1/materials/categories/list")
def list_categories():
    categories = sorted({m["category"] for m in MATERIALS})
    return {"categories": categories, "total": len(categories)}


@app.get("/api/v1/materials/{material_id}", response_model=Material)
def get_material(material_id: str):
    for material in MATERIALS:
        if material["id"] == material_id:
            return material
    raise HTTPException(status_code=404, detail="Material not found")
