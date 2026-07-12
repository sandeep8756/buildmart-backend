from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class WorkerSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    category: str
    experience: int
    hourlyRate: int
    dailyRate: int
    rating: float
    reviews: int
    location: str
    phone: str
    available: bool
    skills: List[str]
    verified: bool


class WorkersListResponse(BaseModel):
    rows: List[Dict[str, Any]]
    columnDefs: List[Dict[str, str]]
    total: int
    message: Optional[str] = None
