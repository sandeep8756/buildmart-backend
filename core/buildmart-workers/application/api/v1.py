import logging
from typing import Optional

import utils.logging_cfg
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from utils.decorators_async import async_log_pre_post, exception_handler

from .service import (
    worker_categories_service,
    worker_detail_service,
    workers_list_service,
)

logger = logging.getLogger("buildmart")
v1 = APIRouter(tags=["Workers Core APIs"])


@v1.get("/health")
@exception_handler
@async_log_pre_post
async def health(request: Request):
    return JSONResponse({"service": "buildmart-workers", "status": "healthy"})


@v1.get("/workers_list")
@exception_handler
@async_log_pre_post
async def workers_list(
    request: Request,
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    available: Optional[bool] = Query(None),
):
    content = await workers_list_service(
        category=category, search=search, available=available
    )
    return JSONResponse(content=content, status_code=200)


@v1.get("/worker_detail/{worker_id}")
@exception_handler
@async_log_pre_post
async def worker_detail(request: Request, worker_id: str):
    content = await worker_detail_service(worker_id)
    return JSONResponse(content=content, status_code=200)


@v1.get("/worker_categories")
@exception_handler
@async_log_pre_post
async def worker_categories(request: Request):
    content = await worker_categories_service()
    return JSONResponse(content=content, status_code=200)
