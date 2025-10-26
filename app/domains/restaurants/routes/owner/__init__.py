"""Owner routes for restaurant management.

This package contains routes for restaurant owners to manage their restaurants
and view their ownership information.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.owner.get_my_restaurant import (
    router as get_my_restaurant_router,
)
from app.domains.restaurants.routes.owner.list_my_restaurants import (
    router as list_my_restaurants_router,
)
from app.domains.restaurants.routes.owner.list_my_team import (
    router as list_my_team_router,
)
from app.domains.restaurants.routes.owner.update_my_restaurant import (
    router as update_my_restaurant_router,
)


# Main owner router for restaurant management
router = APIRouter(prefix="/owner")

# Include all owner routes
router.include_router(list_my_restaurants_router)  # GET /owner/restaurants
router.include_router(get_my_restaurant_router)  # GET /owner/restaurants/{id}
router.include_router(update_my_restaurant_router)  # PATCH /owner/restaurants/{id}
router.include_router(list_my_team_router)  # GET /owner/restaurants/{id}/team


__all__ = ["router"]
