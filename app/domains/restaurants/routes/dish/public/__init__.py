"""Public dish routes.

This module aggregates all publicly accessible dish endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.dish.public import find_all, get


# Create router (no prefix for public routes)
router = APIRouter(tags=["Public - Dishes"])

# Include routes
router.include_router(find_all.router)
router.include_router(get.router)
