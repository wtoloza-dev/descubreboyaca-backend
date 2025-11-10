"""User routes package."""

from fastapi import APIRouter

from app.domains.users.presentation.api.routes import admin


router = APIRouter(prefix="/users")

router.include_router(admin.router, tags=["Users - Admin"])
