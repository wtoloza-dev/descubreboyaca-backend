"""Restaurant API routes.

This package contains the REST API endpoints for restaurants and dishes.
"""

from fastapi import APIRouter

from app.domains.restaurants.presentation.api.routes.dish import router as dishes_router
from app.domains.restaurants.presentation.api.routes.restaurant import (
    router as restaurants_router,
)
from app.domains.restaurants.presentation.graphql import create_graphql_router


# Main router combines all restaurant endpoints
router = APIRouter(prefix="/restaurants")

# Order matters: more specific paths should come before generic ones to avoid conflicts

# Restaurant routes (includes admin, owner, and public)
# Admin routes (prefix: /restaurants/admin)
# - POST /restaurants/admin/
# - DELETE /restaurants/admin/{id}
# - Ownership management endpoints
# Owner routes (prefix: /restaurants/owner)
# - GET /restaurants/owner/restaurants
# - GET /restaurants/owner/restaurants/{id}
# - PATCH /restaurants/owner/restaurants/{id}
# - GET /restaurants/owner/restaurants/{id}/team
# Public routes (no prefix)
# - GET /restaurants
# - GET /restaurants/city/{city}
# - GET /restaurants/favorites
# - GET /restaurants/{id}
router.include_router(restaurants_router)

# Dish routes (includes both public and owner)
# Public:
# - GET /restaurants/{restaurant_id}/dishes
# - GET /restaurants/dishes/{dish_id}
# Owner:
# - POST /restaurants/owner/restaurants/{restaurant_id}/dishes
# - PATCH /restaurants/owner/dishes/{dish_id}
# - DELETE /restaurants/owner/dishes/{dish_id}
router.include_router(dishes_router)

# GraphQL endpoint
# - POST /restaurants/graphql (GraphQL queries/mutations)
# - GET /restaurants/graphql (GraphiQL interface in browser)
graphql_router = create_graphql_router()
router.include_router(graphql_router)


__all__ = ["router"]
