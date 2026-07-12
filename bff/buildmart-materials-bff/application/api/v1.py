"""Materials BFF — proxies UI requests to materials core service."""
import logging
from typing import Optional

import utils.logging_cfg
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from utils.decorators_async import async_log_pre_post, exception_handler

from .service import get_material_bff, list_categories_bff, list_materials_bff

logger = logging.getLogger("buildmart")
v1 = APIRouter(tags=["Materials BFF"])


@v1.get("/health")
async def health_check():
    return {
        "serviceDescription": "buildmart-materials-bff",
        "status": "UP",
    }


@v1.get("/materials_list_bff")
@exception_handler
@async_log_pre_post
async def materials_list_bff(
    request: Request,
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    content, status = await list_materials_bff(category=category, search=search)
    return JSONResponse(content=content, status_code=status)


@v1.get("/material_detail_bff/{material_id}")
@exception_handler
@async_log_pre_post
async def material_detail_bff(request: Request, material_id: str):
    content, status = await get_material_bff(material_id)
    return JSONResponse(content=content, status_code=status)


@v1.get("/material_categories_bff")
@exception_handler
@async_log_pre_post
async def material_categories_bff(request: Request):
    content, status = await list_categories_bff()
    return JSONResponse(content=content, status_code=status)
