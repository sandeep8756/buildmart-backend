"""Workers BFF — proxies UI requests to workers core service."""
import json
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from application.api_workers.service import (
    get_worker_bff,
    list_categories_bff,
    list_workers_bff,
)
from utils.decorators_async import async_log_pre_post, exception_handler

router = APIRouter(tags=["Workers BFF"])


@router.get("/workers_list_bff")
@exception_handler
@async_log_pre_post
async def workers_list_bff(
    request: Request,
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    available: Optional[bool] = Query(None),
):
    content, status = await list_workers_bff(
        category=category, search=search, available=available
    )
    return JSONResponse(content=content, status_code=status)


@router.get("/worker_detail_bff/{worker_id}")
@exception_handler
@async_log_pre_post
async def worker_detail_bff(request: Request, worker_id: str):
    content, status = await get_worker_bff(worker_id)
    return JSONResponse(content=content, status_code=status)


@router.get("/worker_categories_bff")
@exception_handler
@async_log_pre_post
async def worker_categories_bff(request: Request):
    content, status = await list_categories_bff()
    return JSONResponse(content=content, status_code=status)
