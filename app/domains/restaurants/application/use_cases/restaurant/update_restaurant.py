"""Use case for updating an existing restaurant.

This module provides the business logic for updating restaurant information.
"""

from app.domains.restaurants.domain import Restaurant, RestaurantData
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class UpdateRestaurantUseCase:
    """Use case for updating an existing restaurant.

    This use case handles updating restaurant data and ensures
    the restaurant exists before updating.

    Attributes:
        repository: Restaurant repository for data persistence
    """

    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        restaurant_id: str,
        restaurant_data: RestaurantData,
        updated_by: str | None = None,
    ) -> Restaurant:
        """Execute the update restaurant use case.

        Args:
            restaurant_id: ULID of the restaurant to update
            restaurant_data: Updated restaurant data
            updated_by: ULID of the user updating the restaurant

        Returns:
            Restaurant: Updated restaurant

        Raises:
            RestaurantNotFoundException: If restaurant is not found
        """
        updated = await self.repository.update(
            restaurant_id, restaurant_data, updated_by=updated_by
        )
        if not updated:
            raise RestaurantNotFoundException(restaurant_id)
        return updated
