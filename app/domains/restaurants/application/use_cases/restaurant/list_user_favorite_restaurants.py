"""Use case for listing user's favorite restaurants.

This module provides the business logic for retrieving restaurants
that a user has marked as favorites.
"""

from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface
from app.domains.restaurants.domain import Restaurant
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class ListUserFavoriteRestaurantsUseCase:
    """Use case for listing restaurants favorited by a user.

    This use case retrieves all restaurants that a user has marked as favorites,
    using the favorite repository to get the list of favorite entity IDs,
    then fetching the complete restaurant data for each one.

    Attributes:
        restaurant_repository: Restaurant repository for data retrieval
        favorite_repository: Favorite repository for user favorites
    """

    def __init__(
        self,
        restaurant_repository: RestaurantRepositoryInterface,
        favorite_repository: FavoriteRepositoryInterface,
    ) -> None:
        """Initialize the use case with dependencies.

        Args:
            restaurant_repository: Restaurant repository implementation
            favorite_repository: Favorite repository implementation
        """
        self.restaurant_repository = restaurant_repository
        self.favorite_repository = favorite_repository

    async def execute(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Restaurant], int]:
        """Execute the list user favorite restaurants use case.

        Args:
            user_id: ULID of the user
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorite restaurants, total count)

        Example:
            >>> restaurants, total = await use_case.execute(
            ...     user_id="01BX5ZZKBKACTAV9WEVGEMMVS0",
            ...     offset=0,
            ...     limit=10,
            ... )
        """
        # Get user's favorite restaurants
        favorites, total = await self.favorite_repository.get_by_user(
            user_id=user_id,
            entity_type=EntityType.RESTAURANT,
            offset=offset,
            limit=limit,
        )

        # Extract restaurant IDs from favorites
        restaurant_ids = [favorite.entity_id for favorite in favorites]

        # If no favorites, return empty list
        if not restaurant_ids:
            return [], 0

        # Fetch complete restaurant data for each favorite
        # TODO: Optimize with bulk query (get_by_ids method)
        restaurants = []
        for restaurant_id in restaurant_ids:
            restaurant = await self.restaurant_repository.get_by_id(restaurant_id)
            if restaurant:  # Only add if restaurant still exists
                restaurants.append(restaurant)

        return restaurants, total
