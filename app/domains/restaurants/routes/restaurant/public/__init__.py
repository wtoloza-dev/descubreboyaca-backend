"""Public restaurant routes.

This module aggregates all publicly accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant.public.find_all import (
    router as find_all_router,
)
from app.domains.restaurants.routes.restaurant.public.get import (
    router as get_router,
)
from app.domains.restaurants.routes.restaurant.public.list_by_city import (
    router as list_by_city_router,
)
from app.domains.restaurants.routes.restaurant.public.list_favorites import (
    router as list_favorites_router,
)


router = APIRouter()

router.include_router(find_all_router)
router.include_router(list_by_city_router)
router.include_router(list_favorites_router)
router.include_router(get_router)
