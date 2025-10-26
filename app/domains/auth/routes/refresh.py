"""Token refresh route.

This module handles refreshing access tokens using refresh tokens.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.sql import get_auth_service_dependency
from app.domains.auth.schemas import (
    RefreshUserSchemaRequest,
    RefreshUserSchemaResponse,
)
from app.domains.auth.services import AuthService


router = APIRouter()


@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Get a new access token using a refresh token",
)
async def handle_refresh_token(
    request: RefreshUserSchemaRequest,
    auth_service: AuthService = Depends(get_auth_service_dependency),
) -> RefreshUserSchemaResponse:
    """Refresh access token.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        request: Refresh token request
        auth_service: Auth service dependency

    Returns:
        RefreshUserSchemaResponse with new access token

    Raises:
        InvalidTokenException: If refresh token is invalid
        ExpiredTokenException: If refresh token has expired
        UserInactiveException: If user account is inactive
        UserNotFoundException: If user not found
    """
    tokens = await auth_service.refresh_access_token(request.refresh_token)

    return RefreshUserSchemaResponse(
        access_token=tokens.access_token,
        token_type=tokens.token_type,
    )
