from typing import Any, Optional

from pydantic import BaseModel


class MaterialsListBffResponse(BaseModel):
    data: list[dict[str, Any]]
    total: int
    columnDefs: list[dict[str, str]]
    message: Optional[str] = None
