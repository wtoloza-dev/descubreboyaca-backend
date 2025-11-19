"""Transfer restaurant ownership by admin endpoint.

This module provides an endpoint for administrators to transfer primary ownership.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    TransferPrimaryOwnershipUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_transfer_primary_ownership_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.transfer_restaurant_ownership_by_admin import (
    TransferRestaurantOwnershipByAdminSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.post(
    path="/restaurants/{restaurant_id}/owners/{owner_id}/transfer/",
    status_code=status.HTTP_200_OK,
    summary="Transfer primary ownership",
    description="Transfer primary ownership of a restaurant to another owner. The new owner must already be assigned to the restaurant. Only administrators can perform this action.",
)
async def handle_transfer_restaurant_ownership_by_admin(
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
    use_case: Annotated[
        TransferPrimaryOwnershipUseCase,
        Depends(get_transfer_primary_ownership_use_case_dependency),
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> TransferRestaurantOwnershipByAdminSchemaResponse:
    """Transfer primary ownership to another owner.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden transferir ownership.

    This endpoint transfers the primary ownership flag from the current primary owner
    to the specified owner. The new primary owner must already be assigned to the
    restaurant (as owner, manager, or staff).

    Args:
        restaurant_id: ULID of the restaurant
        owner_id: ULID of the new primary owner
        use_case: Transfer primary ownership use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        TransferRestaurantOwnershipByAdminSchemaResponse: Updated ownership relationship of the new primary owner

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if owner not assigned to restaurant
        HTTPException: 404 if restaurant or owner not found
    """
    ownership = await use_case.execute(
        restaurant_id=str(restaurant_id),
        new_owner_id=str(owner_id),
        transferred_by=current_user.id,
    )

    return TransferRestaurantOwnershipByAdminSchemaResponse.model_validate(ownership)
