"""Use case for requiring restaurant ownership with exception.

This module provides the business logic for enforcing ownership
requirements, raising an exception if not met.
"""

from app.domains.auth.domain.exceptions import InsufficientPermissionsException
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class RequireOwnershipUseCase:
    """Use case for verifying that a user owns a restaurant, raise exception if not.

    This use case encapsulates the ownership verification logic,
    preventing routes from directly handling domain exceptions.

    Attributes:
        repository: Restaurant owner repository for data retrieval
    """

    def __init__(
        self,
        repository: RestaurantOwnerRepositoryInterface,
    ) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant owner repository implementation
        """
        self.repository = repository

    async def execute(self, owner_id: str, restaurant_id: str) -> None:
        """Execute the require ownership use case.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Raises:
            InsufficientPermissionsException: If user is not an owner of the restaurant
        """
        is_owner = await self.repository.is_owner_of_restaurant(owner_id, restaurant_id)
        if not is_owner:
            raise InsufficientPermissionsException(
                f"User {owner_id} does not have permission to access restaurant {restaurant_id}"
            )
