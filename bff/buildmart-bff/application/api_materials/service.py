import json
from typing import Any, Optional

from utils.common_async import fetch_get
from utils.properties import Properties

prop = Properties()


async def list_materials_bff(
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> tuple[dict[str, Any], int]:
    params = []
    if category:
        params.append(f"category={category}")
    if search:
        params.append(f"search={search}")
    query = f"?{'&'.join(params)}" if params else ""
    status, raw = await fetch_get(prop.materials_core_url(f"/materials_list{query}"))
    content = json.loads(raw) if raw else {}
    return {
        "data": content.get("rows", []),
        "total": content.get("total", 0),
        "columnDefs": content.get("columnDefs", []),
        "message": content.get("message"),
    }, status


async def get_material_bff(material_id: str) -> tuple[dict[str, Any], int]:
    status, raw = await fetch_get(
        prop.materials_core_url(f"/material_detail/{material_id}")
    )
    content = json.loads(raw) if raw else {}
    return {"data": content, "message": None}, status


async def list_categories_bff() -> tuple[dict[str, Any], int]:
    status, raw = await fetch_get(prop.materials_core_url("/material_categories"))
    content = json.loads(raw) if raw else {}
    return content, status
