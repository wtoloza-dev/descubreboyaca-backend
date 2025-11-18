"""Find my team endpoint.

This module provides an endpoint for restaurant owners to find their team members.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from pydantic import BaseModel, ConfigDict

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    GetOwnersByRestaurantUseCase,
    RequireOwnershipUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_get_owners_by_restaurant_use_case_dependency,
    get_require_ownership_use_case_dependency,
)
from app.domains.users.domain import User


router = APIRouter()


class TeamMemberResponse(BaseModel):
    """Response schema for a team member."""

    owner_id: str
    role: str
    is_primary: bool

    model_config = ConfigDict(from_attributes=True)


class TeamListResponse(BaseModel):
    """Response schema for team list."""

    restaurant_id: str
    team: list[TeamMemberResponse]
    total: int


@router.get(
    path="/restaurants/{restaurant_id}/team/",
    status_code=status.HTTP_200_OK,
    summary="Find my restaurant team",
    description="Find all team members (owners/managers/staff) for a restaurant owned/managed by the current user.",
)
async def handle_find_my_team(
    restaurant_id: Annotated[str, Path(description="ULID of the restaurant")],
    require_ownership_use_case: Annotated[
        RequireOwnershipUseCase, Depends(get_require_ownership_use_case_dependency)
    ],
    get_owners_use_case: Annotated[
        GetOwnersByRestaurantUseCase,
        Depends(get_get_owners_by_restaurant_use_case_dependency),
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> TeamListResponse:
    """Find all team members of a restaurant owned/managed by the current user.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint returns all users who have management rights on this restaurant,
    including their roles and primary owner status. The current user must be an
    owner/manager of the restaurant.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        restaurant_id: ULID of the restaurant
        require_ownership_use_case: Require ownership use case (injected)
        get_owners_use_case: Get owners by restaurant use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        TeamListResponse: List of team members

    Raises:
        InsufficientPermissionsException: If not owner of this restaurant
        RestaurantNotFoundException: If restaurant not found
    """
    # Verify ownership (use case will raise exception if not owner)
    await require_ownership_use_case.execute(
        owner_id=current_user.id,
        restaurant_id=restaurant_id,
    )

    # Get team members
    team_members = await get_owners_use_case.execute(restaurant_id)

    return TeamListResponse(
        restaurant_id=restaurant_id,
        team=[TeamMemberResponse.model_validate(member) for member in team_members],
        total=len(team_members),
    )
