"""Restaurant use cases dependencies.

This module provides dependency injection factories for all restaurant-related
use cases.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.audit.infrastructure.dependencies import (
    get_archive_repository_dependency,
)
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface
from app.domains.favorites.infrastructure.dependencies import (
    get_favorite_repository_dependency,
)
from app.domains.restaurants.application.use_cases.restaurant import (
    CountRestaurantsUseCase,
    CreateRestaurantUseCase,
    DeleteRestaurantUseCase,
    FindRestaurantByIdUseCase,
    FindRestaurantsUseCase,
    ListRestaurantsByCityUseCase,
    ListUserFavoriteRestaurantsUseCase,
    UpdateRestaurantUseCase,
)
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.domains.restaurants.infrastructure.dependencies.restaurant.repository import (
    get_restaurant_repository_dependency,
)


def get_create_restaurant_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> CreateRestaurantUseCase:
    """Factory to create a CreateRestaurantUseCase instance.

    Args:
        repository: Restaurant repository (injected via Depends)

    Returns:
        CreateRestaurantUseCase: Configured use case instance
    """
    return CreateRestaurantUseCase(repository)


def get_find_restaurant_by_id_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> FindRestaurantByIdUseCase:
    """Factory to create a FindRestaurantByIdUseCase instance.

    Args:
        repository: Restaurant repository (injected via Depends)

    Returns:
        FindRestaurantByIdUseCase: Configured use case instance
    """
    return FindRestaurantByIdUseCase(repository)


def get_find_restaurants_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> FindRestaurantsUseCase:
    """Factory to create a FindRestaurantsUseCase instance.

    Args:
        repository: Restaurant repository (injected via Depends)

    Returns:
        FindRestaurantsUseCase: Configured use case instance
    """
    return FindRestaurantsUseCase(repository)


def get_count_restaurants_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> CountRestaurantsUseCase:
    """Factory to create a CountRestaurantsUseCase instance.

    Args:
        repository: Restaurant repository (injected via Depends)

    Returns:
        CountRestaurantsUseCase: Configured use case instance
    """
    return CountRestaurantsUseCase(repository)


def get_list_restaurants_by_city_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> ListRestaurantsByCityUseCase:
    """Factory to create a ListRestaurantsByCityUseCase instance.

    Args:
        repository: Restaurant repository (injected via Depends)

    Returns:
        ListRestaurantsByCityUseCase: Configured use case instance
    """
    return ListRestaurantsByCityUseCase(repository)


def get_update_restaurant_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> UpdateRestaurantUseCase:
    """Factory to create an UpdateRestaurantUseCase instance.

    Args:
        repository: Restaurant repository (injected via Depends)

    Returns:
        UpdateRestaurantUseCase: Configured use case instance
    """
    return UpdateRestaurantUseCase(repository)


def get_delete_restaurant_use_case_dependency(
    restaurant_repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
    archive_repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> DeleteRestaurantUseCase:
    """Factory to create a DeleteRestaurantUseCase instance.

    This use case requires both restaurant and archive repositories
    for atomic delete with archiving (Unit of Work pattern).

    Args:
        restaurant_repository: Restaurant repository (injected via Depends)
        archive_repository: Archive repository (injected via Depends)

    Returns:
        DeleteRestaurantUseCase: Configured use case instance

    Note:
        Both repositories receive the same session, ensuring they participate
        in the same transaction for atomic operations.
    """
    return DeleteRestaurantUseCase(restaurant_repository, archive_repository)


def get_list_user_favorite_restaurants_use_case_dependency(
    restaurant_repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
    favorite_repository: Annotated[
        FavoriteRepositoryInterface, Depends(get_favorite_repository_dependency)
    ],
) -> ListUserFavoriteRestaurantsUseCase:
    """Factory to create a ListUserFavoriteRestaurantsUseCase instance.

    This use case requires both restaurant and favorite repositories
    to retrieve favorite restaurants for a user.

    Args:
        restaurant_repository: Restaurant repository (injected via Depends)
        favorite_repository: Favorite repository (injected via Depends)

    Returns:
        ListUserFavoriteRestaurantsUseCase: Configured use case instance
    """
    return ListUserFavoriteRestaurantsUseCase(
        restaurant_repository, favorite_repository
    )
