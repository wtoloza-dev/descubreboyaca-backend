"""Update owner role endpoint.

This module provides an endpoint for administrators to update an owner's role.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    UpdateOwnerRoleUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_update_owner_role_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.update_owner_role import (
    UpdateOwnerRoleSchemaRequest,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.common.ownership import (
    OwnershipSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.patch(
    path="/restaurants/{restaurant_id}/owners/{owner_id}/role/",
    status_code=status.HTTP_200_OK,
    summary="Update an owner's role",
    description="Change the role of an owner/manager/staff member. Only administrators can perform this action.",
)
async def handle_update_owner_role(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    owner_id: Annotated[
        ULID,
        Path(
            description="ULID of the owner",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    request: UpdateOwnerRoleSchemaRequest,
    use_case: Annotated[
        UpdateOwnerRoleUseCase, Depends(get_update_owner_role_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> OwnershipSchemaResponse:
    """Update the role of an owner/manager/staff.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden actualizar roles.

    This endpoint allows administrators to change a user's role in restaurant management.
    Valid roles are: owner, manager, staff.

    Args:
        restaurant_id: ULID of the restaurant
        owner_id: ULID of the owner whose role to update
        request: Role update request with new role
        use_case: Update owner role use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        OwnershipSchemaResponse: Updated ownership relationship

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if invalid role or owner not found
        HTTPException: 404 if ownership relationship not found
    """
    ownership = await use_case.execute(
        restaurant_id=str(restaurant_id),
        owner_id=str(owner_id),
        new_role=request.role,
        updated_by=current_user.id,
    )

    return OwnershipSchemaResponse.model_validate(ownership)
