"""Core router — materials endpoints."""
import logging
from typing import Optional

import utils.logging_cfg
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from utils.decorators_async import async_log_pre_post, exception_handler

from .service import (
    material_categories_service,
    material_detail_service,
    materials_list_service,
)

logger = logging.getLogger("buildmart")
v1 = APIRouter(tags=["Materials Core APIs"])


@v1.get("/health")
@exception_handler
@async_log_pre_post
async def health(request: Request):
    return JSONResponse({"service": "buildmart-materials", "status": "healthy"})


@v1.get("/materials_list")
@exception_handler
@async_log_pre_post
async def materials_list(
    request: Request,
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    content = await materials_list_service(category=category, search=search)
    return JSONResponse(content=content, status_code=200)


@v1.get("/material_detail/{material_id}")
@exception_handler
@async_log_pre_post
async def material_detail(request: Request, material_id: str):
    content = await material_detail_service(material_id)
    return JSONResponse(content=content, status_code=200)


@v1.get("/material_categories")
@exception_handler
@async_log_pre_post
async def material_categories(request: Request):
    content = await material_categories_service()
    return JSONResponse(content=content, status_code=200)
