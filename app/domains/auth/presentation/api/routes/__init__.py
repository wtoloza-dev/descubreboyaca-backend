"""Auth routes.

This module contains API route handlers for authentication endpoints.
"""

from fastapi import APIRouter

from app.domains.auth.presentation.api.routes import (
    google_callback,
    google_login,
    login,
    me,
    refresh,
    register,
)


router = APIRouter(prefix="/auth", tags=["Auth"])

# Register all auth routes
router.include_router(register.router)
router.include_router(login.router)
router.include_router(refresh.router)
router.include_router(me.router)
router.include_router(google_login.router)
router.include_router(google_callback.router)

__all__ = ["router"]
