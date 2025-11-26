"""Review routes.

This module provides API routes for the reviews domain.
"""

from fastapi import APIRouter

from .public import router as public_router
from .user import router as user_router


router = APIRouter(prefix="/reviews")

# Public routes (no authentication required)
router.include_router(public_router, tags=["Reviews - Public"])

# User routes (authentication required)
router.include_router(user_router, tags=["Reviews - User"])

__all__ = ["router"]
