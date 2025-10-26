"""Admin routes for restaurant management.

This package contains routes for administrators to manage restaurants,
including creating, deleting, and managing restaurant ownership.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.admin.assign_owner import (
    router as assign_owner_router,
)
from app.domains.restaurants.routes.admin.create import router as create_router
from app.domains.restaurants.routes.admin.delete import router as delete_router
from app.domains.restaurants.routes.admin.list_owners import (
    router as list_owners_router,
)
from app.domains.restaurants.routes.admin.remove_owner import (
    router as remove_owner_router,
)
from app.domains.restaurants.routes.admin.transfer_ownership import (
    router as transfer_ownership_router,
)
from app.domains.restaurants.routes.admin.update_owner_role import (
    router as update_owner_role_router,
)


# Main admin router for restaurant management
router = APIRouter(prefix="/admin")

# Include all admin routes
router.include_router(create_router)  # POST /admin/restaurants
router.include_router(delete_router)  # DELETE /admin/restaurants/{id}
router.include_router(assign_owner_router)  # POST /admin/restaurants/{id}/owners
router.include_router(list_owners_router)  # GET /admin/restaurants/{id}/owners
router.include_router(
    remove_owner_router
)  # DELETE /admin/restaurants/{id}/owners/{owner_id}
router.include_router(
    update_owner_role_router
)  # PATCH /admin/restaurants/{id}/owners/{owner_id}/role
router.include_router(
    transfer_ownership_router
)  # POST /admin/restaurants/{id}/owners/{owner_id}/transfer


__all__ = ["router"]
