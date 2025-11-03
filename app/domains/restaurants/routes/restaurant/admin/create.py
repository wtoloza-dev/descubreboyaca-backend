"""Create restaurant endpoint.

This module provides a simplified endpoint for creating restaurants with minimal fields (admin only).
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_service_dependency,
)
from app.domains.restaurants.domain import RestaurantData
from app.domains.restaurants.schemas.restaurant.admin.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)
from app.domains.restaurants.services import RestaurantService


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new restaurant (Admin only)",
    description="Create a new restaurant with essential information only. "
    "Additional details can be added later through update operations. "
    "Only administrators can perform this action.",
)
async def handle_create_restaurant(
    request: Annotated[CreateRestaurantSchemaRequest, Body()],
    service: Annotated[RestaurantService, Depends(get_restaurant_service_dependency)],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> CreateRestaurantSchemaResponse:
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
        service: Restaurant service (injected)
        admin_user: Authenticated admin user (injected)

    Returns:
        CreateRestaurantSchemaResponse: Created restaurant with all fields

    Raises:
        HTTPException: 400 if validation fails
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not admin
    """
    restaurant_data = RestaurantData(**request.model_dump())
    restaurant = await service.create_restaurant(
        restaurant_data, created_by=admin_user.id
    )
    return CreateRestaurantSchemaResponse.model_validate(restaurant)
