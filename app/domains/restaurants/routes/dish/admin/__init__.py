"""Admin dish routes.

This module aggregates all admin-accessible dish endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.dish.admin import create, delete, update


router = APIRouter(prefix="/admin", tags=["Admin - Dishes"])

router.include_router(create.router)
router.include_router(update.router)
router.include_router(delete.router)
