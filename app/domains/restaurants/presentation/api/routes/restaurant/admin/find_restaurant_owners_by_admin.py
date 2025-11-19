"""Find restaurant owners by admin endpoint.

This module provides an endpoint for administrators to find all owners of a restaurant.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    GetOwnersByRestaurantUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_get_owners_by_restaurant_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.find_restaurant_owners_by_admin import (
    FindRestaurantOwnersByAdminSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.get(
    path="/restaurants/{restaurant_id}/owners/",
    status_code=status.HTTP_200_OK,
    summary="Find all owners of a restaurant",
    description="Find all users who have ownership/management rights on a restaurant. Only administrators can access this information.",
)
async def handle_find_restaurant_owners_by_admin(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    use_case: Annotated[
        GetOwnersByRestaurantUseCase,
        Depends(get_get_owners_by_restaurant_use_case_dependency),
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> FindRestaurantOwnersByAdminSchemaResponse:
    """Find all owners/managers/staff of a restaurant.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden ver owners.

    This endpoint returns all users who have been assigned to manage this restaurant,
    including their roles (owner, manager, staff) and whether they are the primary owner.

    Args:
        restaurant_id: ULID of the restaurant
        use_case: Get owners by restaurant use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        FindRestaurantOwnersByAdminSchemaResponse: List of owners with their roles

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 404 if restaurant not found
    """
    owners = await use_case.execute(str(restaurant_id))

    return FindRestaurantOwnersByAdminSchemaResponse(
        restaurant_id=str(restaurant_id),
        owners=owners,
        total=len(owners),
    )
