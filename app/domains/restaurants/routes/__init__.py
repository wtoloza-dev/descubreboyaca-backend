"""Restaurant API routes.

This package contains the REST API endpoints for restaurants.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.admin import router as admin_router
from app.domains.restaurants.routes.owner import router as owner_router
from app.domains.restaurants.routes.public import router as public_router


# Main router combines all restaurant endpoints
router = APIRouter(prefix="/restaurants")

# Order matters: more specific paths should come before generic ones to avoid conflicts

# Admin routes (prefix: /restaurants/admin)
# - POST /restaurants/admin/
# - DELETE /restaurants/admin/{id}
# - Ownership management endpoints
router.include_router(admin_router, tags=["Admin - Restaurants"])

# Owner routes (prefix: /restaurants/owner)
# - GET /restaurants/owner/restaurants
# - GET /restaurants/owner/restaurants/{id}
# - PATCH /restaurants/owner/restaurants/{id}
# - GET /restaurants/owner/restaurants/{id}/team
router.include_router(owner_router, tags=["Owner - Restaurants"])

# Public restaurant routes (no prefix)
# - GET /restaurants
# - GET /restaurants/city/{city}
# - GET /restaurants/favorites
# - GET /restaurants/{id}
router.include_router(public_router, tags=["Public - Restaurants"])


__all__ = ["router"]
