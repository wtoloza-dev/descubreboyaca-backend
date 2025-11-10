"""Admin audit routes.

This module aggregates all admin-accessible audit endpoints.
"""

from fastapi import APIRouter

from app.domains.audit.presentation.api.routes.admin import hard_delete


router = APIRouter(prefix="/admin")

router.include_router(hard_delete.router)
