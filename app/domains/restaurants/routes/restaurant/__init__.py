"""Restaurant routes.

This module aggregates all restaurant-related endpoints (public, admin, and owner).
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant import admin, owner, public


router = APIRouter()

router.include_router(admin.router, tags=["Admin - Restaurants"])
router.include_router(owner.router, tags=["Owner - Restaurants"])
router.include_router(public.router, tags=["Public - Restaurants"])
