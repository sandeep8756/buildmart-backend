from typing import Any, Dict

from application.api.repository import DELIVERY_OPTIONS
from application.api.schemas import DeliveryQuoteRequest


async def delivery_options_service() -> Dict[str, Any]:
    return {
        "rows": list(DELIVERY_OPTIONS),
        "total": len(DELIVERY_OPTIONS),
        "message": None,
    }


async def delivery_option_service(option_id: str) -> Dict[str, Any]:
    for option in DELIVERY_OPTIONS:
        if option["id"] == option_id:
            return option
    raise ValueError("Delivery option not found")


async def delivery_quote_service(request: DeliveryQuoteRequest) -> Dict[str, Any]:
    for option in DELIVERY_OPTIONS:
        if option["id"] == request.option_id:
            total = option["basePrice"] + int(option["pricePerKm"] * request.distance_km)
            return {
                "optionId": option["id"],
                "optionName": option["name"],
                "distanceKm": request.distance_km,
                "basePrice": option["basePrice"],
                "pricePerKm": option["pricePerKm"],
                "totalPrice": total,
                "estimatedTime": option["estimatedTime"],
            }
    raise ValueError("Delivery option not found")
