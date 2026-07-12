import json
from typing import Any

from utils.common_async import fetch_get, fetch_post
from utils.properties import Properties

from .schemas import DeliveryQuoteRequest


async def list_delivery_options_bff() -> tuple[dict[str, Any], int]:
    status, raw = await fetch_get(Properties.core_url("/delivery_options"))
    content = json.loads(raw) if raw else {}
    return {
        "data": content.get("rows", []),
        "total": content.get("total", 0),
        "message": content.get("message"),
    }, status


async def get_delivery_option_bff(option_id: str) -> tuple[dict[str, Any], int]:
    status, raw = await fetch_get(
        Properties.core_url(f"/delivery_option/{option_id}")
    )
    content = json.loads(raw) if raw else {}
    return {"data": content, "message": None}, status


async def delivery_quote_bff(
    body: DeliveryQuoteRequest,
) -> tuple[dict[str, Any], int]:
    status, raw = await fetch_post(
        Properties.core_url("/delivery_quote"),
        headers={"Content-Type": "application/json"},
        body=body.model_dump_json(by_alias=True),
    )
    content = json.loads(raw) if raw else {}
    return {"data": content, "message": "Delivery quote calculated"}, status
