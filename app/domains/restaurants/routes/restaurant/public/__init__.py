"""Public restaurant routes.

This module aggregates all publicly accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant.public import (
    get,
    list,
    list_by_city,
    list_favorites,
)


router = APIRouter(tags=["Public - Restaurants"])

router.include_router(list.router)
router.include_router(list_by_city.router)
router.include_router(list_favorites.router)
router.include_router(get.router)
