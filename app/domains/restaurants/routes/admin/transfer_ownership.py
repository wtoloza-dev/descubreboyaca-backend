"""Transfer ownership endpoint.

This module provides an endpoint for administrators to transfer primary ownership.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import (
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.schemas.ownership import OwnershipSchemaResponse
from app.domains.restaurants.services import RestaurantOwnerService


router = APIRouter()


@router.post(
    path="/restaurants/{restaurant_id}/owners/{owner_id}/transfer",
    status_code=status.HTTP_200_OK,
    summary="Transfer primary ownership",
    description="Transfer primary ownership of a restaurant to another owner. The new owner must already be assigned to the restaurant. Only administrators can perform this action.",
)
async def handle_transfer_ownership(
    restaurant_id: str,
    owner_id: str,
    service: RestaurantOwnerService = Depends(get_restaurant_owner_service_dependency),
    current_user: User = Depends(require_admin_dependency),
) -> OwnershipSchemaResponse:
    """Transfer primary ownership to another owner.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden transferir ownership.

    This endpoint transfers the primary ownership flag from the current primary owner
    to the specified owner. The new primary owner must already be assigned to the
    restaurant (as owner, manager, or staff).

    Args:
        restaurant_id: ULID of the restaurant
        owner_id: ULID of the new primary owner
        service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        OwnershipSchemaResponse: Updated ownership relationship of the new primary owner

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if owner not assigned to restaurant
        HTTPException: 404 if restaurant or owner not found
    """
    ownership = await service.transfer_ownership(
        restaurant_id=restaurant_id,
        new_primary_owner_id=owner_id,
        updated_by=current_user.id,
    )

    return OwnershipSchemaResponse.model_validate(ownership)
