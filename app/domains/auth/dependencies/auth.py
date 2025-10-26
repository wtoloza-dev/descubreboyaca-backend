"""Auth dependencies.

This module provides dependency injection for authentication and authorization.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from app.domains.auth.dependencies.sql import get_auth_service_dependency
from app.domains.auth.domain import User
from app.domains.auth.domain.enums import UserRole
from app.domains.auth.domain.exceptions import (
    ExpiredTokenException,
    InsufficientPermissionsException,
    InvalidTokenException,
    UserInactiveException,
    UserNotFoundException,
)
from app.domains.auth.services import AuthService


# OAuth2 password bearer for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=True)

# Optional OAuth2 scheme (doesn't raise error if no token)
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

# HTTP Bearer for actual token extraction
http_bearer = HTTPBearer(auto_error=False)
optional_http_bearer = HTTPBearer(auto_error=False)


async def get_current_user_dependency(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dependency)],
) -> User:
    """Get the current authenticated user from JWT token.

    This dependency extracts the JWT token from the Authorization header,
    validates it, and returns the corresponding user.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        credentials: HTTP Bearer credentials with JWT token (None if not provided)
        auth_service: Auth service from dependency

    Returns:
        Current authenticated user

    Raises:
        InvalidTokenException: If token is missing, invalid or malformed
        ExpiredTokenException: If token has expired
        UserInactiveException: If user account is inactive
        UserNotFoundException: If user no longer exists
    """
    if credentials is None:
        raise InvalidTokenException("Missing authentication token")

    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    return user


async def get_optional_user_dependency(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(optional_http_bearer)
    ],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dependency)],
) -> User | None:
    """Get the current authenticated user if token is provided.

    This is an optional version of get_current_user_dependency that returns None
    if no token is provided instead of raising an error.

    Args:
        credentials: Optional HTTP Bearer credentials with JWT token
        auth_service: Auth service from dependency

    Returns:
        Current authenticated user or None if no token provided
    """
    if credentials is None:
        return None

    try:
        token = credentials.credentials
        user = await auth_service.get_current_user(token)
        return user
    except (
        InvalidTokenException,
        ExpiredTokenException,
        UserInactiveException,
        UserNotFoundException,
    ):
        return None


async def require_admin_dependency(
    current_user: Annotated[User, Depends(get_current_user_dependency)],
) -> User:
    """Require that the current user has admin role.

    This dependency can be used to protect admin-only endpoints.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if they are an admin

    Raises:
        InsufficientPermissionsException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise InsufficientPermissionsException(UserRole.ADMIN)

    return current_user


async def require_owner_dependency(
    current_user: Annotated[User, Depends(get_current_user_dependency)],
) -> User:
    """Require that the current user has owner role.

    This dependency can be used to protect owner-only endpoints.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if they are an owner

    Raises:
        InsufficientPermissionsException: If user is not an owner
    """
    if current_user.role != UserRole.OWNER:
        raise InsufficientPermissionsException(UserRole.OWNER)

    return current_user


async def verify_restaurant_ownership(
    restaurant_id: str,
    current_user: User,
) -> bool:
    """Verify that the current user is an owner of the specified restaurant.

    This is a utility function that should be called within route handlers
    to verify ownership of a specific restaurant.

    Args:
        restaurant_id: ULID of the restaurant to verify ownership
        current_user: Current authenticated user

    Returns:
        True if user is owner

    Raises:
        InsufficientPermissionsException: If user is not an owner of this restaurant
    """
    # Import here to avoid circular dependency
    from app.domains.restaurants.dependencies.sql import (
        get_restaurant_owner_repository_dependency,
    )
    from app.shared.dependencies.sql import get_async_session_dependency

    # Get a session and repository to check ownership
    async for session in get_async_session_dependency():
        repo = get_restaurant_owner_repository_dependency(session)
        is_owner = await repo.is_owner_of_restaurant(current_user.id, restaurant_id)

        if not is_owner:
            raise InsufficientPermissionsException(
                f"User {current_user.id} does not have ownership permissions for restaurant {restaurant_id}"
            )

        return True

    # This should never happen if the async generator works correctly
    raise InsufficientPermissionsException("Failed to verify restaurant ownership")
