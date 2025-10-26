"""Dish routes.

This module aggregates all dish-related endpoints (public, owner, and admin).
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.dish import admin, owner, public


router = APIRouter()

router.include_router(admin.router)
router.include_router(owner.router)
router.include_router(public.router)
