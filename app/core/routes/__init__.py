"""Core application routes.

This package contains core routes for health checks, root endpoints,
and other application-wide endpoints.
"""

from fastapi import APIRouter

from app.core.settings import settings

from .health import router as health_router
from .main import router as main_router


# Create main core router
router = APIRouter(tags=["Core API"], include_in_schema=settings.DEBUG)

# Include sub-routers
router.include_router(health_router)
router.include_router(main_router)


__all__ = ["router"]
