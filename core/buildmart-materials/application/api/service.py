"""Service layer — materials business logic."""
from typing import Any, Dict, List, Optional

from application.api.repository import MATERIALS, _COLUMN_DEFS


async def materials_list_service(
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> Dict[str, Any]:
    rows: List[dict] = list(MATERIALS)
    if category:
        rows = [m for m in rows if m["category"] == category]
    if search:
        q = search.lower()
        rows = [
            m for m in rows
            if q in m["name"].lower() or q in m["brand"].lower()
        ]
    message = None if rows else "No materials found."
    return {
        "rows": rows,
        "columnDefs": list(_COLUMN_DEFS),
        "total": len(rows),
        "message": message,
    }


async def material_detail_service(material_id: str) -> Dict[str, Any]:
    for material in MATERIALS:
        if material["id"] == material_id:
            return material
    raise ValueError("Material not found")


async def material_categories_service() -> Dict[str, Any]:
    categories = sorted({m["category"] for m in MATERIALS})
    return {"categories": categories, "total": len(categories)}
