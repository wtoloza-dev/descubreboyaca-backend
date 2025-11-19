"""Admin restaurant routes.

This module aggregates all admin-accessible restaurant endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.presentation.api.routes.restaurant.admin import (
    assign_restaurant_owner_by_admin,
    create_restaurant_by_admin,
    delete_restaurant_by_admin,
    find_restaurant_owners_by_admin,
    remove_restaurant_owner_by_admin,
    transfer_restaurant_ownership_by_admin,
    update_restaurant_owner_role_by_admin,
)


router = APIRouter(prefix="/admin")

router.include_router(create_restaurant_by_admin.router)
router.include_router(delete_restaurant_by_admin.router)
router.include_router(assign_restaurant_owner_by_admin.router)
router.include_router(find_restaurant_owners_by_admin.router)
router.include_router(remove_restaurant_owner_by_admin.router)
router.include_router(update_restaurant_owner_role_by_admin.router)
router.include_router(transfer_restaurant_ownership_by_admin.router)
