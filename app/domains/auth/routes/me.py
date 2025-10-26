"""Current user route.

This module handles getting the current authenticated user's information.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import get_current_user_dependency
from app.domains.auth.domain import User
from app.domains.auth.schemas import MeUserSchemaResponse, UserSchemaResponse


router = APIRouter()


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get the currently authenticated user's information",
)
async def handle_get_me(
    current_user: User = Depends(get_current_user_dependency),
) -> MeUserSchemaResponse:
    """Get current authenticated user.

    Args:
        current_user: Current user from JWT token

    Returns:
        MeUserSchemaResponse with user data
    """
    return MeUserSchemaResponse(user=UserSchemaResponse.model_validate(current_user))
