"""Aggregates materials, workers, and delivery BFF routers."""
from fastapi import APIRouter

from application.api_delivery.router import router as delivery_router
from application.api_materials.router import router as materials_router
from application.api_workers.router import router as workers_router

router = APIRouter(tags=["BuildMart BFF"])
router.include_router(materials_router)
router.include_router(workers_router)
router.include_router(delivery_router)
