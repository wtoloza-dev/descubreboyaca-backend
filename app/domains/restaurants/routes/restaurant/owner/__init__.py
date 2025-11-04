"""Owner restaurant routes.

This module aggregates all owner-accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant.owner import (
    find_my_restaurant,
    find_my_restaurants,
    find_my_team,
    update_my_restaurant,
)


router = APIRouter(prefix="/owner")

router.include_router(find_my_restaurants.router)
router.include_router(find_my_restaurant.router)
router.include_router(update_my_restaurant.router)
router.include_router(find_my_team.router)
