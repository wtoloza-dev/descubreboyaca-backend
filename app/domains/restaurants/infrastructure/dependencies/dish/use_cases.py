"""Dish use cases dependencies.

This module provides dependency injection factories for all dish-related
use cases.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.audit.infrastructure.dependencies import (
    get_archive_repository_dependency,
)
from app.domains.restaurants.application.use_cases.dish import (
    CreateDishUseCase,
    DeleteDishUseCase,
    FindDishByIdUseCase,
    ListDishesUseCase,
    ListRestaurantDishesUseCase,
    ToggleDishAvailabilityUseCase,
    UpdateDishUseCase,
)
from app.domains.restaurants.domain.interfaces import (
    DishRepositoryInterface,
    RestaurantRepositoryInterface,
)
from app.domains.restaurants.infrastructure.dependencies.dish.repository import (
    get_dish_repository_dependency,
)
from app.domains.restaurants.infrastructure.dependencies.restaurant.repository import (
    get_restaurant_repository_dependency,
)


def get_create_dish_use_case_dependency(
    dish_repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
    restaurant_repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> CreateDishUseCase:
    """Factory to create a CreateDishUseCase instance.

    This use case requires both dish and restaurant repositories
    to validate restaurant existence before creating the dish.

    Args:
        dish_repository: Dish repository (injected via Depends)
        restaurant_repository: Restaurant repository (injected via Depends)

    Returns:
        CreateDishUseCase: Configured use case instance
    """
    return CreateDishUseCase(dish_repository, restaurant_repository)


def get_find_dish_by_id_use_case_dependency(
    repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
) -> FindDishByIdUseCase:
    """Factory to create a FindDishByIdUseCase instance.

    Args:
        repository: Dish repository (injected via Depends)

    Returns:
        FindDishByIdUseCase: Configured use case instance
    """
    return FindDishByIdUseCase(repository)


def get_list_restaurant_dishes_use_case_dependency(
    dish_repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
    restaurant_repository: Annotated[
        RestaurantRepositoryInterface, Depends(get_restaurant_repository_dependency)
    ],
) -> ListRestaurantDishesUseCase:
    """Factory to create a ListRestaurantDishesUseCase instance.

    This use case requires both repositories to validate restaurant
    existence and retrieve its dishes.

    Args:
        dish_repository: Dish repository (injected via Depends)
        restaurant_repository: Restaurant repository (injected via Depends)

    Returns:
        ListRestaurantDishesUseCase: Configured use case instance
    """
    return ListRestaurantDishesUseCase(dish_repository, restaurant_repository)


def get_update_dish_use_case_dependency(
    repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
) -> UpdateDishUseCase:
    """Factory to create an UpdateDishUseCase instance.

    Args:
        repository: Dish repository (injected via Depends)

    Returns:
        UpdateDishUseCase: Configured use case instance
    """
    return UpdateDishUseCase(repository)


def get_delete_dish_use_case_dependency(
    dish_repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
    archive_repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> DeleteDishUseCase:
    """Factory to create a DeleteDishUseCase instance.

    This use case requires both dish and archive repositories
    for atomic delete with archiving (Unit of Work pattern).

    Args:
        dish_repository: Dish repository (injected via Depends)
        archive_repository: Archive repository (injected via Depends)

    Returns:
        DeleteDishUseCase: Configured use case instance

    Note:
        Both repositories receive the same session, ensuring they participate
        in the same transaction for atomic operations.
    """
    return DeleteDishUseCase(dish_repository, archive_repository)


def get_toggle_dish_availability_use_case_dependency(
    repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
) -> ToggleDishAvailabilityUseCase:
    """Factory to create a ToggleDishAvailabilityUseCase instance.

    Args:
        repository: Dish repository (injected via Depends)

    Returns:
        ToggleDishAvailabilityUseCase: Configured use case instance
    """
    return ToggleDishAvailabilityUseCase(repository)


def get_list_dishes_use_case_dependency(
    repository: Annotated[
        DishRepositoryInterface, Depends(get_dish_repository_dependency)
    ],
) -> ListDishesUseCase:
    """Factory to create a ListDishesUseCase instance.

    Args:
        repository: Dish repository (injected via Depends)

    Returns:
        ListDishesUseCase: Configured use case instance
    """
    return ListDishesUseCase(repository)
