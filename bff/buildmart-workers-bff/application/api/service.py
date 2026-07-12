import json
from typing import Any, Optional

from utils.common_async import fetch_get
from utils.properties import Properties


async def list_workers_bff(
    category: Optional[str] = None,
    search: Optional[str] = None,
    available: Optional[bool] = None,
) -> tuple[dict[str, Any], int]:
    params = []
    if category:
        params.append(f"category={category}")
    if search:
        params.append(f"search={search}")
    if available is not None:
        params.append(f"available={str(available).lower()}")
    query = f"?{'&'.join(params)}" if params else ""
    status, raw = await fetch_get(Properties.core_url(f"/workers_list{query}"))
    content = json.loads(raw) if raw else {}
    return {
        "data": content.get("rows", []),
        "total": content.get("total", 0),
        "columnDefs": content.get("columnDefs", []),
        "message": content.get("message"),
    }, status


async def get_worker_bff(worker_id: str) -> tuple[dict[str, Any], int]:
    status, raw = await fetch_get(
        Properties.core_url(f"/worker_detail/{worker_id}")
    )
    content = json.loads(raw) if raw else {}
    return {"data": content, "message": None}, status


async def list_categories_bff() -> tuple[dict[str, Any], int]:
    status, raw = await fetch_get(Properties.core_url("/worker_categories"))
    content = json.loads(raw) if raw else {}
    return content, status
