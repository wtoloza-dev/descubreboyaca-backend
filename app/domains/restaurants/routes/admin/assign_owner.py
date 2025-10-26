"""Assign owner endpoint.

This module provides an endpoint for administrators to assign owners to restaurants.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import (
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.schemas.ownership import (
    AssignOwnerSchemaRequest,
    OwnershipSchemaResponse,
)
from app.domains.restaurants.services import RestaurantOwnerService


router = APIRouter()


@router.post(
    path="/restaurants/{restaurant_id}/owners",
    status_code=status.HTTP_201_CREATED,
    summary="Assign an owner to a restaurant",
    description="Assign a user as owner/manager/staff of a restaurant. Only administrators can perform this action.",
)
async def handle_assign_owner(
    restaurant_id: str,
    request: AssignOwnerSchemaRequest,
    service: RestaurantOwnerService = Depends(get_restaurant_owner_service_dependency),
    current_user: User = Depends(require_admin_dependency),
) -> OwnershipSchemaResponse:
    """Assign an owner to a restaurant.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden asignar owners.

    This endpoint allows administrators to assign a user as owner, manager, or staff
    of a restaurant. If is_primary is True, this will automatically unset any existing
    primary owner.

    Args:
        restaurant_id: ULID of the restaurant
        request: Owner assignment request with owner_id, role, and is_primary
        service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        OwnershipSchemaResponse: Created ownership relationship

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if owner already assigned or validation fails
        HTTPException: 404 if restaurant or user not found
    """
    ownership = await service.assign_owner(
        restaurant_id=restaurant_id,
        owner_id=request.owner_id,
        role=request.role,
        is_primary=request.is_primary,
        assigned_by=current_user.id,
    )

    return OwnershipSchemaResponse.model_validate(ownership)
