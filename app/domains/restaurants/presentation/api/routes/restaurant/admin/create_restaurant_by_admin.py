"""Create restaurant by admin endpoint.

This module provides an endpoint for administrators to create restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.restaurant import (
    CreateRestaurantUseCase,
)
from app.domains.restaurants.domain import RestaurantData
from app.domains.restaurants.infrastructure.dependencies import (
    get_create_restaurant_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.create_restaurant_by_admin import (
    CreateRestaurantByAdminSchemaRequest,
    CreateRestaurantByAdminSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new restaurant (Admin only)",
    description="Create a new restaurant with essential information only. "
    "Additional details can be added later through update operations. "
    "Only administrators can perform this action.",
)
async def handle_create_restaurant_by_admin(
    request: Annotated[CreateRestaurantByAdminSchemaRequest, Body()],
    use_case: Annotated[
        CreateRestaurantUseCase, Depends(get_create_restaurant_use_case_dependency)
    ],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> CreateRestaurantByAdminSchemaResponse:
    """Create a new restaurant with minimal required fields.

    **Requiere rol ADMIN**: Solo administradores pueden crear restaurantes.

    This endpoint simplifies restaurant creation by requiring only essential fields:
    - name: Restaurant name
    - address: Physical address
    - city: City location
    - phone: Contact phone number (required)
    - location: GPS coordinates (optional, can be obtained via geocoding)
    - description: Brief description (optional)

    All other fields will have sensible defaults:
    - state: "Boyacá"
    - country: "Colombia"
    - cuisine_types: []
    - features: []

    Args:
        request: Simplified restaurant creation request
        use_case: Create restaurant use case (injected)
        admin_user: Authenticated admin user (injected)

    Returns:
        CreateRestaurantByAdminSchemaResponse: Created restaurant with all fields

    Raises:
        HTTPException: 400 if validation fails
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not admin
    """
    restaurant_data = RestaurantData(**request.model_dump())
    restaurant = await use_case.execute(restaurant_data, created_by=admin_user.id)
    return CreateRestaurantByAdminSchemaResponse.model_validate(restaurant)
