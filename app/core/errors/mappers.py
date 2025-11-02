"""Exception mappers for converting domain exceptions to HTTP responses.

This module provides mapping logic to convert domain exceptions into appropriate
HTTP status codes and error responses while maintaining clean architecture boundaries.
"""

from fastapi import status

from app.domains.auth.domain.exceptions import (
    AuthenticationException,
    ExpiredTokenException,
    InsufficientPermissionsException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserInactiveException,
    UserNotFoundException,
)
from app.domains.favorites.domain.exceptions import (
    FavoriteAlreadyExistsException,
    FavoriteNotFoundException,
)
from app.domains.restaurants.domain.exceptions import (
    CannotRemovePrimaryOwnerException,
    DishNotFoundException,
    InvalidCuisineTypeException,
    InvalidOwnerRoleException,
    InvalidPriceLevelException,
    OwnerNotAssignedException,
    OwnershipAlreadyExistsException,
    OwnershipNotFoundException,
    RestaurantAlreadyExistsException,
    RestaurantNotFoundException,
)
from app.shared.domain.exceptions import (
    AlreadyExistsException,
    DomainException,
    MissingHeaderException,
    NotFoundException,
    ValidationException,
)


class DomainExceptionMapper:
    """Maps domain exceptions to HTTP status codes and error details."""

    # Mapping of domain exceptions to HTTP status codes
    EXCEPTION_STATUS_MAP: dict[type[DomainException], int] = {
        # Base exceptions - Generic mappings
        NotFoundException: status.HTTP_404_NOT_FOUND,
        AlreadyExistsException: status.HTTP_409_CONFLICT,
        ValidationException: status.HTTP_400_BAD_REQUEST,
        MissingHeaderException: status.HTTP_400_BAD_REQUEST,
        # Auth domain - Authentication errors
        AuthenticationException: status.HTTP_401_UNAUTHORIZED,
        InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
        InvalidTokenException: status.HTTP_401_UNAUTHORIZED,
        ExpiredTokenException: status.HTTP_401_UNAUTHORIZED,
        UserInactiveException: status.HTTP_403_FORBIDDEN,
        InsufficientPermissionsException: status.HTTP_403_FORBIDDEN,
        # Auth domain - User management errors
        UserNotFoundException: status.HTTP_404_NOT_FOUND,
        UserAlreadyExistsException: status.HTTP_409_CONFLICT,
        # Restaurants domain - Restaurant errors
        RestaurantNotFoundException: status.HTTP_404_NOT_FOUND,
        RestaurantAlreadyExistsException: status.HTTP_409_CONFLICT,
        InvalidCuisineTypeException: status.HTTP_400_BAD_REQUEST,
        InvalidPriceLevelException: status.HTTP_400_BAD_REQUEST,
        # Restaurants domain - Dish errors
        DishNotFoundException: status.HTTP_404_NOT_FOUND,
        # Restaurants domain - Ownership errors
        OwnershipNotFoundException: status.HTTP_404_NOT_FOUND,
        OwnershipAlreadyExistsException: status.HTTP_409_CONFLICT,
        CannotRemovePrimaryOwnerException: status.HTTP_400_BAD_REQUEST,
        InvalidOwnerRoleException: status.HTTP_400_BAD_REQUEST,
        OwnerNotAssignedException: status.HTTP_403_FORBIDDEN,
        # Favorites domain - Favorite errors
        FavoriteNotFoundException: status.HTTP_404_NOT_FOUND,
        FavoriteAlreadyExistsException: status.HTTP_409_CONFLICT,
    }

    @classmethod
    def get_status_code(cls, exception: DomainException) -> int:
        """Get HTTP status code for a domain exception.

        Args:
            exception: The domain exception to map

        Returns:
            HTTP status code appropriate for the exception type
        """
        exception_type = type(exception)
        return cls.EXCEPTION_STATUS_MAP.get(
            exception_type, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @classmethod
    def get_error_detail(
        cls, exception: DomainException
    ) -> dict[str, str | dict[str, str]]:
        """Get error detail dictionary for HTTP response.

        Args:
            exception: The domain exception to convert

        Returns:
            Dictionary containing error details for HTTP response
        """
        return {
            "error_code": exception.error_code,
            "message": exception.message,
            "context": exception.context,
        }
