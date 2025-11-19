"""Assign restaurant owner by admin endpoint.

This module provides an endpoint for administrators to assign owners to restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    AssignOwnerUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_assign_owner_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.assign_restaurant_owner_by_admin import (
    AssignRestaurantOwnerByAdminSchemaRequest,
    AssignRestaurantOwnerByAdminSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.post(
    path="/restaurants/{restaurant_id}/owners/",
    status_code=status.HTTP_201_CREATED,
    summary="Assign an owner to a restaurant",
    description="Assign a user as owner/manager/staff of a restaurant. Only administrators can perform this action.",
)
async def handle_assign_restaurant_owner_by_admin(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    request: AssignRestaurantOwnerByAdminSchemaRequest,
    use_case: Annotated[
        AssignOwnerUseCase, Depends(get_assign_owner_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> AssignRestaurantOwnerByAdminSchemaResponse:
    """Assign an owner to a restaurant.

    **Authentication required**: Only administrators (ADMIN) can assign owners.

    This endpoint allows administrators to assign a user as owner, manager, or staff
    of a restaurant. If is_primary is True, this will automatically unset any existing
    primary owner.

    Args:
        restaurant_id: ULID of the restaurant
        request: Owner assignment request with owner_id, role, and is_primary
        use_case: Assign owner use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        AssignRestaurantOwnerByAdminSchemaResponse: Created ownership relationship

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if owner already assigned or validation fails
        HTTPException: 404 if restaurant or user not found
    """
    ownership = await use_case.execute(
        restaurant_id=str(restaurant_id),
        owner_id=request.owner_id,
        role=request.role,
        is_primary=request.is_primary,
        assigned_by=current_user.id,
    )

    return AssignRestaurantOwnerByAdminSchemaResponse.model_validate(ownership)
