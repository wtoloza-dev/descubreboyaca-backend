"""User login route.

This module handles user login with email and password.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.application.services import AuthService
from app.domains.auth.infrastructure.dependencies.sql import get_auth_service_dependency
from app.domains.auth.presentation.api.schemas import (
    LoginUserSchemaRequest,
    LoginUserSchemaResponse,
    UserSchemaResponse,
)


router = APIRouter()


@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user with email and password",
)
async def handle_login(
    request: Annotated[LoginUserSchemaRequest, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dependency)],
) -> LoginUserSchemaResponse:
    """Login user with email and password.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        request: Login request with email and password
        auth_service: Auth service dependency

    Returns:
        LoginUserSchemaResponse with JWT tokens and user data

    Raises:
        InvalidCredentialsException: If credentials are invalid
        UserInactiveException: If user account is inactive
    """
    tokens, user = await auth_service.login(
        email=request.email,
        password=request.password,
    )

    return LoginUserSchemaResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token or "",
        token_type=tokens.token_type,
        user=UserSchemaResponse.model_validate(user),
    )
