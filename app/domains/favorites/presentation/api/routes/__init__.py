"""Favorites API routes.

This package contains the REST API endpoints for favorites.
"""

from fastapi import APIRouter

from app.domains.favorites.presentation.api.routes.add import router as add_router
from app.domains.favorites.presentation.api.routes.check import router as check_router
from app.domains.favorites.presentation.api.routes.find_all import (
    router as find_all_router,
)
from app.domains.favorites.presentation.api.routes.remove import router as remove_router


# Main router combines all favorite endpoints
router = APIRouter(prefix="/favorites")

# Register all routes
router.include_router(add_router, tags=["Favorites"])
router.include_router(remove_router, tags=["Favorites"])
router.include_router(find_all_router, tags=["Favorites"])
router.include_router(check_router, tags=["Favorites"])

__all__ = ["router"]
