"""Delete restaurant endpoint.

This module provides an endpoint for deleting restaurants (admin only).
The deletion follows an archive-first pattern to maintain audit trail.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import get_restaurant_service_dependency
from app.domains.restaurants.schemas.restaurant.delete import (
    DeleteRestaurantSchemaRequest,
)
from app.domains.restaurants.services import RestaurantService


router = APIRouter()


@router.delete(
    path="/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a restaurant (Admin only)",
    description="""Permanently delete a restaurant from the active database.

This operation:
1. Archives the complete restaurant record for audit purposes
2. Permanently removes the restaurant from the active database
3. Maintains referential integrity (handles related records)

**Archive Pattern**: The restaurant data is preserved in the archive table
with metadata about who deleted it, when, and why. This maintains a complete
audit trail while keeping the active database clean and performant.

**Required Role**: ADMIN
""",
)
async def handle_delete_restaurant(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant to delete",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    request_body: DeleteRestaurantSchemaRequest = Body(
        default=DeleteRestaurantSchemaRequest(),
        description="Optional deletion metadata (note explaining why)",
    ),
    service: RestaurantService = Depends(get_restaurant_service_dependency),
    admin_user: User = Depends(require_admin_dependency),
) -> None:
    """Delete a restaurant permanently with archiving.

    **Archive-First Pattern**:
    This endpoint implements the archive-first deletion pattern:
    1. Validates restaurant exists
    2. Creates archive record with:
       - Complete restaurant data (JSON)
       - Deletion timestamp
       - Admin user ID who performed deletion
       - Optional note explaining reason
    3. Performs hard delete from restaurants table

    This pattern provides:
    - **Audit trail**: Who, when, why deleted
    - **Data recovery**: Complete data preserved
    - **Performance**: Active DB stays clean
    - **Compliance**: Regulatory requirements

    **Required Role**: ADMIN

    Args:
        restaurant_id: ULID of the restaurant to delete (validated automatically)
        request_body: Optional deletion metadata (note)
        service: Restaurant service (injected)
        admin_user: Authenticated admin user (injected)

    Returns:
        None: 204 No Content on success

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 403: If not admin role
        HTTPException 404: If restaurant not found
        HTTPException 422: If restaurant_id format is invalid (not a valid ULID)

    Example:
        DELETE /api/v1/admin/restaurants/01HQZX123456789ABCDEFGHIJK
        {
            "note": "Restaurant permanently closed"
        }

        Response: 204 No Content
    """
    # Delete restaurant with archive
    # Service handles:
    # 1. Get restaurant (raises RestaurantNotFoundException if not found)
    # 2. Archive complete record with metadata
    # 3. Delete from active table
    await service.delete_restaurant(
        restaurant_id=str(restaurant_id),
        deleted_by=admin_user.id,
        note=request_body.note,
    )
