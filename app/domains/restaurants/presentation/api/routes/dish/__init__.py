"""Dish routes.

This module aggregates all dish-related endpoints (public, owner, and admin).
"""

from fastapi import APIRouter

from app.domains.restaurants.presentation.api.routes.dish import admin, owner, public


router = APIRouter()

router.include_router(admin.router, tags=["Dishes - Admin"])
router.include_router(owner.router, tags=["Dishes - Owner"])
router.include_router(public.router, tags=["Dishes - Public"])
