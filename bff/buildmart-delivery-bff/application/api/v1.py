"""Delivery BFF — proxies UI requests to delivery core service."""
import logging

import utils.logging_cfg
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.decorators_async import async_log_pre_post, exception_handler

from .schemas import DeliveryQuoteRequest
from .service import (
    delivery_quote_bff,
    get_delivery_option_bff,
    list_delivery_options_bff,
)

logger = logging.getLogger("buildmart")
v1 = APIRouter(tags=["Delivery BFF"])


@v1.get("/health")
async def health_check():
    return {
        "serviceDescription": "buildmart-delivery-bff",
        "status": "UP",
    }


@v1.get("/delivery_options_bff")
@exception_handler
@async_log_pre_post
async def delivery_options_bff(request: Request):
    content, status = await list_delivery_options_bff()
    return JSONResponse(content=content, status_code=status)


@v1.get("/delivery_option_bff/{option_id}")
@exception_handler
@async_log_pre_post
async def delivery_option_bff(request: Request, option_id: str):
    content, status = await get_delivery_option_bff(option_id)
    return JSONResponse(content=content, status_code=status)


@v1.post("/delivery_quote_bff")
@exception_handler
@async_log_pre_post
async def delivery_quote_bff_endpoint(request: Request, body: DeliveryQuoteRequest):
    content, status = await delivery_quote_bff(body)
    return JSONResponse(content=content, status_code=status)
