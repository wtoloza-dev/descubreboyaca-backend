"""Update owner role endpoint.

This module provides an endpoint for administrators to update an owner's role.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import (
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.ownership import (
    OwnershipSchemaResponse,
    UpdateOwnerRoleSchemaRequest,
)
from app.domains.restaurants.services import RestaurantOwnerService


router = APIRouter()


@router.patch(
    path="/restaurants/{restaurant_id}/owners/{owner_id}/role",
    status_code=status.HTTP_200_OK,
    summary="Update an owner's role",
    description="Change the role of an owner/manager/staff member. Only administrators can perform this action.",
)
async def handle_update_owner_role(
    restaurant_id: str,
    owner_id: str,
    request: UpdateOwnerRoleSchemaRequest,
    service: RestaurantOwnerService = Depends(get_restaurant_owner_service_dependency),
    current_user: User = Depends(require_admin_dependency),
) -> OwnershipSchemaResponse:
    """Update the role of an owner/manager/staff.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden actualizar roles.

    This endpoint allows administrators to change a user's role in restaurant management.
    Valid roles are: owner, manager, staff.

    Args:
        restaurant_id: ULID of the restaurant
        owner_id: ULID of the owner whose role to update
        request: Role update request with new role
        service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        OwnershipSchemaResponse: Updated ownership relationship

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if invalid role or owner not found
        HTTPException: 404 if ownership relationship not found
    """
    ownership = await service.update_owner_role(
        restaurant_id=restaurant_id,
        owner_id=owner_id,
        role=request.role,
        updated_by=current_user.id,
    )

    return OwnershipSchemaResponse.model_validate(ownership)
