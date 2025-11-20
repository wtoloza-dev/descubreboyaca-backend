"""Status API routes.

This package contains routes for application status and information endpoints.
"""

from fastapi import APIRouter

from app.core.settings import settings

from .health import router as health_router
from .health_db import router as health_db_router
from .root import router as root_router


# Create main status router
router = APIRouter(tags=["Status"], include_in_schema=settings.DEBUG)

# Include sub-routers
router.include_router(health_router)
router.include_router(health_db_router)
router.include_router(root_router)


__all__ = ["router"]
