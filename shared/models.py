from typing import Literal

from pydantic import BaseModel, Field

MaterialCategory = Literal[
    "cement", "steel", "bricks", "sand", "tiles",
    "paint", "wood", "plumbing", "electrical", "hardware",
]

WorkerCategory = Literal[
    "carpenter", "plumber", "electrician", "mason", "painter",
    "maid", "welder", "tile-worker", "ac-technician", "gardener",
    "security", "driver", "interior-designer", "architect",
]


class Material(BaseModel):
    id: str
    name: str
    category: MaterialCategory
    unit: str
    price: float
    brand: str
    description: str
    in_stock: bool = Field(alias="inStock")
    delivery_available: bool = Field(alias="deliveryAvailable")
    min_order: int = Field(alias="minOrder")
    rating: float
    supplier: str

    model_config = {"populate_by_name": True}


class Worker(BaseModel):
    id: str
    name: str
    category: WorkerCategory
    experience: int
    hourly_rate: int = Field(alias="hourlyRate")
    daily_rate: int = Field(alias="dailyRate")
    rating: float
    reviews: int
    location: str
    phone: str
    available: bool
    skills: list[str]
    verified: bool

    model_config = {"populate_by_name": True}


class DeliveryOption(BaseModel):
    id: str
    name: str
    description: str
    base_price: int = Field(alias="basePrice")
    price_per_km: int = Field(alias="pricePerKm")
    estimated_time: str = Field(alias="estimatedTime")
    max_weight: str = Field(alias="maxWeight")
    coverage: str

    model_config = {"populate_by_name": True}


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str = "1.0.0"
