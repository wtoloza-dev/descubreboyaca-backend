"""Review routes.

This module provides API routes for the reviews domain.
"""

from fastapi import APIRouter

from .user import router as user_router


router = APIRouter()

# User routes (authentication required)
router.include_router(user_router, prefix="/reviews", tags=["Reviews - User"])

__all__ = ["router"]
