import logging

import utils.logging_cfg
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.decorators_async import async_log_pre_post, exception_handler

from .schemas import DeliveryQuoteRequest
from .service import (
    delivery_option_service,
    delivery_options_service,
    delivery_quote_service,
)

logger = logging.getLogger("buildmart")
v1 = APIRouter(tags=["Delivery Core APIs"])


@v1.get("/health")
@exception_handler
@async_log_pre_post
async def health(request: Request):
    return JSONResponse({"service": "buildmart-delivery", "status": "healthy"})


@v1.get("/delivery_options")
@exception_handler
@async_log_pre_post
async def delivery_options(request: Request):
    content = await delivery_options_service()
    return JSONResponse(content=content, status_code=200)


@v1.get("/delivery_option/{option_id}")
@exception_handler
@async_log_pre_post
async def delivery_option(request: Request, option_id: str):
    content = await delivery_option_service(option_id)
    return JSONResponse(content=content, status_code=200)


@v1.post("/delivery_quote")
@exception_handler
@async_log_pre_post
async def delivery_quote(request: Request, body: DeliveryQuoteRequest):
    content = await delivery_quote_service(body)
    return JSONResponse(content=content, status_code=200)
