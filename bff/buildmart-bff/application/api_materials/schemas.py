from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class MaterialRow(BaseModel):
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


class MaterialsListBffResponse(BaseModel):
    data: list[dict[str, Any]]
    total: int
    columnDefs: list[dict[str, str]]
    message: Optional[str] = None
