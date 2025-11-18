"""Restaurant owner use cases.

This package contains all use cases related to restaurant ownership operations.
Each use case represents a single business operation.
"""

from app.domains.restaurants.application.use_cases.restaurant_owner.assign_owner import (
    AssignOwnerUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.check_is_owner import (
    CheckIsOwnerUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.get_owners_by_restaurant import (
    GetOwnersByRestaurantUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.get_primary_owner import (
    GetPrimaryOwnerUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.get_restaurants_by_owner import (
    GetRestaurantsByOwnerUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.list_restaurant_owners import (
    ListRestaurantOwnersUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.list_user_restaurants import (
    ListUserRestaurantsUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.remove_owner import (
    RemoveOwnerUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.require_ownership import (
    RequireOwnershipUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.transfer_primary_ownership import (
    TransferPrimaryOwnershipUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.update_owner_role import (
    UpdateOwnerRoleUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner.verify_ownership import (
    VerifyOwnershipUseCase,
)


__all__ = [
    "AssignOwnerUseCase",
    "CheckIsOwnerUseCase",
    "GetOwnersByRestaurantUseCase",
    "GetPrimaryOwnerUseCase",
    "GetRestaurantsByOwnerUseCase",
    "ListRestaurantOwnersUseCase",
    "ListUserRestaurantsUseCase",
    "RemoveOwnerUseCase",
    "RequireOwnershipUseCase",
    "TransferPrimaryOwnershipUseCase",
    "UpdateOwnerRoleUseCase",
    "VerifyOwnershipUseCase",
]
