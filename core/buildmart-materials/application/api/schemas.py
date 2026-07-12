"""Pydantic schemas for materials core APIs."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class MaterialSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    category: str
    unit: str
    price: float
    brand: str
    description: str
    inStock: bool
    deliveryAvailable: bool
    minOrder: int
    rating: float
    supplier: str


class MaterialsListResponse(BaseModel):
    rows: List[Dict[str, Any]]
    columnDefs: List[Dict[str, str]]
    total: int
    message: Optional[str] = None
