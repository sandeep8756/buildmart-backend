import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from shared.models import DeliveryOption, HealthResponse
from data import DELIVERY_OPTIONS

app = FastAPI(
    title="Delivery Core Service",
    description="Core microservice for delivery options and pricing",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DeliveryQuoteRequest(BaseModel):
    option_id: str = Field(alias="optionId")
    distance_km: float = Field(alias="distanceKm", gt=0)

    model_config = {"populate_by_name": True}


class DeliveryQuoteResponse(BaseModel):
    option_id: str = Field(alias="optionId")
    option_name: str = Field(alias="optionName")
    distance_km: float = Field(alias="distanceKm")
    base_price: int = Field(alias="basePrice")
    price_per_km: int = Field(alias="pricePerKm")
    total_price: int = Field(alias="totalPrice")
    estimated_time: str = Field(alias="estimatedTime")

    model_config = {"populate_by_name": True}


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(service="delivery-service", status="healthy")


@app.get("/api/v1/delivery", response_model=list[DeliveryOption])
def list_delivery_options():
    return DELIVERY_OPTIONS


@app.get("/api/v1/delivery/{option_id}", response_model=DeliveryOption)
def get_delivery_option(option_id: str):
    for option in DELIVERY_OPTIONS:
        if option["id"] == option_id:
            return option
    raise HTTPException(status_code=404, detail="Delivery option not found")


@app.post("/api/v1/delivery/quote", response_model=DeliveryQuoteResponse)
def calculate_quote(request: DeliveryQuoteRequest):
    for option in DELIVERY_OPTIONS:
        if option["id"] == request.option_id:
            total = option["basePrice"] + int(option["pricePerKm"] * request.distance_km)
            return DeliveryQuoteResponse(
                optionId=option["id"],
                optionName=option["name"],
                distanceKm=request.distance_km,
                basePrice=option["basePrice"],
                pricePerKm=option["pricePerKm"],
                totalPrice=total,
                estimatedTime=option["estimatedTime"],
            )
    raise HTTPException(status_code=404, detail="Delivery option not found")
