"""Public restaurant routes.

This module aggregates all publicly accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.presentation.api.routes.restaurant.public.find_all_restaurants import (
    router as find_all_restaurants_router,
)
from app.domains.restaurants.presentation.api.routes.restaurant.public.find_favorite_restaurants import (
    router as find_favorite_restaurants_router,
)
from app.domains.restaurants.presentation.api.routes.restaurant.public.find_restaurant_by_city import (
    router as find_restaurant_by_city_router,
)
from app.domains.restaurants.presentation.api.routes.restaurant.public.find_restaurant_by_id import (
    router as find_restaurant_by_id_router,
)


router = APIRouter()

router.include_router(find_all_restaurants_router)
router.include_router(find_restaurant_by_city_router)
router.include_router(find_favorite_restaurants_router)
router.include_router(find_restaurant_by_id_router)
