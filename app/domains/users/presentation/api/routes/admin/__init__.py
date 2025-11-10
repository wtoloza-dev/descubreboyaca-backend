"""Admin user management routes.

This module aggregates all admin-accessible user management endpoints.
"""

from fastapi import APIRouter

from app.domains.users.presentation.api.routes.admin import create, delete, find_all


router = APIRouter(prefix="/admin")

router.include_router(create.router)
router.include_router(find_all.router)
router.include_router(delete.router)
