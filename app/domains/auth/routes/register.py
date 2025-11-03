"""User registration route.

This module handles user registration with email and password.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.dependencies.sql import get_auth_service_dependency
from app.domains.auth.schemas import (
    RegisterUserSchemaRequest,
    RegisterUserSchemaResponse,
    UserSchemaResponse,
)
from app.domains.auth.services import AuthService


router = APIRouter()


@router.post(
    path="/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user with email and password",
)
async def handle_register(
    request: Annotated[RegisterUserSchemaRequest, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dependency)],
) -> RegisterUserSchemaResponse:
    """Register a new user.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        request: Registration request with email, password, and full_name
        auth_service: Auth service dependency

    Returns:
        RegisterUserSchemaResponse with created user data

    Raises:
        UserAlreadyExistsException: If email already exists
    """
    user = await auth_service.register(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )

    return RegisterUserSchemaResponse(
        user=UserSchemaResponse.model_validate(user),
        message="User registered successfully",
    )
