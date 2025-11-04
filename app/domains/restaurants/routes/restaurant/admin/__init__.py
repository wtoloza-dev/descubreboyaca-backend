"""Admin restaurant routes.

This module aggregates all admin-accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.restaurant.admin import (
    assign_owner,
    create,
    delete,
    find_owners,
    remove_owner,
    transfer_ownership,
    update_owner_role,
)


router = APIRouter(prefix="/admin")

router.include_router(create.router)
router.include_router(delete.router)
router.include_router(assign_owner.router)
router.include_router(find_owners.router)
router.include_router(remove_owner.router)
router.include_router(update_owner_role.router)
router.include_router(transfer_ownership.router)
