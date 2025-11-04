"""Public restaurant routes.

This module aggregates all publicly accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant.public.find_all import (
    router as find_all_router,
)
from app.domains.restaurants.routes.restaurant.public.find_by_city import (
    router as find_by_city_router,
)
from app.domains.restaurants.routes.restaurant.public.find_by_id import (
    router as find_by_id_router,
)
from app.domains.restaurants.routes.restaurant.public.find_favorites import (
    router as find_favorites_router,
)


router = APIRouter()

router.include_router(find_all_router)
router.include_router(find_by_city_router)
router.include_router(find_favorites_router)
router.include_router(find_by_id_router)
