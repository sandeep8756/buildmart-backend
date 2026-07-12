from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DeliveryOptionSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    description: str
    basePrice: int
    pricePerKm: int
    estimatedTime: str
    maxWeight: str
    coverage: str


class DeliveryQuoteRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    option_id: str = Field(alias="optionId")
    distance_km: float = Field(alias="distanceKm", gt=0)


class DeliveryListResponse(BaseModel):
    rows: List[Dict[str, Any]]
    total: int
    message: Optional[str] = None
