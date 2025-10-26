"""Restaurant domain exceptions.

This module provides exception classes specific to the restaurants
bounded context, representing violations of restaurant business rules.
"""

from app.domains.restaurants.domain.exceptions.cannot_remove_primary_owner import (
    CannotRemovePrimaryOwnerException,
)
from app.domains.restaurants.domain.exceptions.invalid_cuisine_type import (
    InvalidCuisineTypeException,
)
from app.domains.restaurants.domain.exceptions.invalid_owner_role import (
    InvalidOwnerRoleException,
)
from app.domains.restaurants.domain.exceptions.invalid_price_level import (
    InvalidPriceLevelException,
)
from app.domains.restaurants.domain.exceptions.owner_not_assigned import (
    OwnerNotAssignedException,
)
from app.domains.restaurants.domain.exceptions.ownership_already_exists import (
    OwnershipAlreadyExistsException,
)
from app.domains.restaurants.domain.exceptions.ownership_not_found import (
    OwnershipNotFoundException,
)
from app.domains.restaurants.domain.exceptions.restaurant_already_exists import (
    RestaurantAlreadyExistsException,
)
from app.domains.restaurants.domain.exceptions.restaurant_not_found import (
    RestaurantNotFoundException,
)


__all__ = [
    # Restaurant exceptions
    "RestaurantNotFoundException",
    "RestaurantAlreadyExistsException",
    "InvalidCuisineTypeException",
    "InvalidPriceLevelException",
    # Ownership exceptions
    "OwnershipNotFoundException",
    "OwnershipAlreadyExistsException",
    "CannotRemovePrimaryOwnerException",
    "InvalidOwnerRoleException",
    "OwnerNotAssignedException",
]
