"""Audit API routes.

This package contains the REST API endpoints for audit operations.
"""

from fastapi import APIRouter

from app.domains.audit.presentation.api.routes.admin import router as admin_router


# Main router combines all audit endpoints
router = APIRouter(prefix="/audit")

# Admin routes (prefix: /audit/admin)
# - DELETE /audit/admin/archives - Hard delete archive record
router.include_router(admin_router, tags=["Audit - Admin"])


__all__ = ["router"]
