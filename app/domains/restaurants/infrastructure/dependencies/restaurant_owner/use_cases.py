"""Restaurant owner use cases dependencies.

This module provides dependency injection factories for all restaurant ownership-related
use cases.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.restaurants.application.use_cases.restaurant_owner import (
    AssignOwnerUseCase,
    CheckIsOwnerUseCase,
    GetOwnersByRestaurantUseCase,
    GetPrimaryOwnerUseCase,
    GetRestaurantsByOwnerUseCase,
    ListRestaurantOwnersUseCase,
    ListUserRestaurantsUseCase,
    RemoveOwnerUseCase,
    RequireOwnershipUseCase,
    TransferPrimaryOwnershipUseCase,
    UpdateOwnerRoleUseCase,
    VerifyOwnershipUseCase,
)
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)
from app.domains.restaurants.infrastructure.dependencies.restaurant_owner.repository import (
    get_restaurant_owner_repository_dependency,
)


def get_assign_owner_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> AssignOwnerUseCase:
    """Factory to create an AssignOwnerUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        AssignOwnerUseCase: Configured use case instance
    """
    return AssignOwnerUseCase(repository)


def get_remove_owner_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> RemoveOwnerUseCase:
    """Factory to create a RemoveOwnerUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        RemoveOwnerUseCase: Configured use case instance
    """
    return RemoveOwnerUseCase(repository)


def get_update_owner_role_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> UpdateOwnerRoleUseCase:
    """Factory to create an UpdateOwnerRoleUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        UpdateOwnerRoleUseCase: Configured use case instance
    """
    return UpdateOwnerRoleUseCase(repository)


def get_transfer_primary_ownership_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> TransferPrimaryOwnershipUseCase:
    """Factory to create a TransferPrimaryOwnershipUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        TransferPrimaryOwnershipUseCase: Configured use case instance
    """
    return TransferPrimaryOwnershipUseCase(repository)


def get_list_restaurant_owners_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> ListRestaurantOwnersUseCase:
    """Factory to create a ListRestaurantOwnersUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        ListRestaurantOwnersUseCase: Configured use case instance
    """
    return ListRestaurantOwnersUseCase(repository)


def get_list_user_restaurants_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> ListUserRestaurantsUseCase:
    """Factory to create a ListUserRestaurantsUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        ListUserRestaurantsUseCase: Configured use case instance
    """
    return ListUserRestaurantsUseCase(repository)


def get_get_primary_owner_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> GetPrimaryOwnerUseCase:
    """Factory to create a GetPrimaryOwnerUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        GetPrimaryOwnerUseCase: Configured use case instance
    """
    return GetPrimaryOwnerUseCase(repository)


def get_verify_ownership_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> VerifyOwnershipUseCase:
    """Factory to create a VerifyOwnershipUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        VerifyOwnershipUseCase: Configured use case instance
    """
    return VerifyOwnershipUseCase(repository)


def get_check_is_owner_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> CheckIsOwnerUseCase:
    """Factory to create a CheckIsOwnerUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        CheckIsOwnerUseCase: Configured use case instance
    """
    return CheckIsOwnerUseCase(repository)


def get_require_ownership_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> RequireOwnershipUseCase:
    """Factory to create a RequireOwnershipUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        RequireOwnershipUseCase: Configured use case instance
    """
    return RequireOwnershipUseCase(repository)


def get_get_restaurants_by_owner_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> GetRestaurantsByOwnerUseCase:
    """Factory to create a GetRestaurantsByOwnerUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        GetRestaurantsByOwnerUseCase: Configured use case instance
    """
    return GetRestaurantsByOwnerUseCase(repository)


def get_get_owners_by_restaurant_use_case_dependency(
    repository: Annotated[
        RestaurantOwnerRepositoryInterface,
        Depends(get_restaurant_owner_repository_dependency),
    ],
) -> GetOwnersByRestaurantUseCase:
    """Factory to create a GetOwnersByRestaurantUseCase instance.

    Args:
        repository: Restaurant owner repository (injected via Depends)

    Returns:
        GetOwnersByRestaurantUseCase: Configured use case instance
    """
    return GetOwnersByRestaurantUseCase(repository)
