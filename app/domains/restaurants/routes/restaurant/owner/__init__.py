"""Owner restaurant routes.

This module aggregates all owner-accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant.owner import (
    get_my_restaurant,
    list_my_restaurants,
    list_my_team,
    update_my_restaurant,
)


router = APIRouter(prefix="/owner", tags=["Owner - Restaurants"])

router.include_router(list_my_restaurants.router)
router.include_router(get_my_restaurant.router)
router.include_router(update_my_restaurant.router)
router.include_router(list_my_team.router)
