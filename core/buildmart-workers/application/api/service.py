from typing import Any, Dict, List, Optional

from application.api.repository import WORKERS, _COLUMN_DEFS


async def workers_list_service(
    category: Optional[str] = None,
    search: Optional[str] = None,
    available: Optional[bool] = None,
) -> Dict[str, Any]:
    rows: List[dict] = list(WORKERS)
    if category:
        rows = [w for w in rows if w["category"] == category]
    if search:
        q = search.lower()
        rows = [
            w for w in rows
            if q in w["name"].lower()
            or q in w["location"].lower()
            or any(q in s.lower() for s in w["skills"])
        ]
    if available is not None:
        rows = [w for w in rows if w["available"] == available]
    message = None if rows else "No workers found."
    return {
        "rows": rows,
        "columnDefs": list(_COLUMN_DEFS),
        "total": len(rows),
        "message": message,
    }


async def worker_detail_service(worker_id: str) -> Dict[str, Any]:
    for worker in WORKERS:
        if worker["id"] == worker_id:
            return worker
    raise ValueError("Worker not found")


async def worker_categories_service() -> Dict[str, Any]:
    categories = sorted({w["category"] for w in WORKERS})
    return {"categories": categories, "total": len(categories)}
