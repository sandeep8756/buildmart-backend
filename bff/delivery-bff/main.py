import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

CORE_URL = os.getenv("DELIVERY_CORE_URL", "http://localhost:8003")

app = FastAPI(
    title="Delivery BFF",
    description="Backend-for-Frontend microservice for delivery",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuoteRequest(BaseModel):
    option_id: str = Field(alias="optionId")
    distance_km: float = Field(alias="distanceKm", gt=0)

    model_config = {"populate_by_name": True}


@app.get("/health")
def health():
    return {"service": "delivery-bff", "status": "healthy", "coreUrl": CORE_URL}


@app.get("/api/v1/delivery")
async def list_delivery_options():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/delivery")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
        options = response.json()
    return {
        "data": options,
        "total": len(options),
        "message": "Delivery options fetched successfully",
    }


@app.get("/api/v1/delivery/{option_id}")
async def get_delivery_option(option_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CORE_URL}/api/v1/delivery/{option_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Delivery option not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
    return {"data": response.json(), "message": "Delivery option fetched successfully"}


@app.post("/api/v1/delivery/quote")
async def get_quote(request: QuoteRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CORE_URL}/api/v1/delivery/quote",
            json={"optionId": request.option_id, "distanceKm": request.distance_km},
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Delivery option not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Core service error")
    return {"data": response.json(), "message": "Delivery quote calculated successfully"}
