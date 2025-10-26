"""Public routes for restaurants.

This package contains publicly accessible REST API endpoints for restaurants.
These routes do not require authentication.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.public.get import router as get_router
from app.domains.restaurants.routes.public.list import router as list_router
from app.domains.restaurants.routes.public.list_by_city import (
    router as list_by_city_router,
)
from app.domains.restaurants.routes.public.list_favorites import (
    router as list_favorites_router,
)


# Main public router for restaurants
router = APIRouter()

# Include all public routes
router.include_router(list_router)  # GET /restaurants
router.include_router(list_by_city_router)  # GET /restaurants/city/{city}
router.include_router(list_favorites_router)  # GET /restaurants/favorites
router.include_router(get_router)  # GET /restaurants/{id}


__all__ = ["router"]
