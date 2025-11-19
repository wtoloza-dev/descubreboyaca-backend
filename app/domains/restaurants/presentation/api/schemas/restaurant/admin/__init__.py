"""Admin restaurant schemas package."""

from .assign_restaurant_owner_by_admin import (
    AssignRestaurantOwnerByAdminSchemaRequest,
    AssignRestaurantOwnerByAdminSchemaResponse,
)
from .create_restaurant_by_admin import (
    CreateRestaurantByAdminSchemaRequest,
    CreateRestaurantByAdminSchemaResponse,
)
from .delete_restaurant_by_admin import DeleteRestaurantByAdminSchemaRequest
from .find_restaurant_owners_by_admin import (
    FindRestaurantOwnersByAdminSchemaItem,
    FindRestaurantOwnersByAdminSchemaResponse,
)
from .transfer_restaurant_ownership_by_admin import (
    TransferRestaurantOwnershipByAdminSchemaResponse,
)
from .update_restaurant_owner_role_by_admin import (
    UpdateRestaurantOwnerRoleByAdminSchemaRequest,
    UpdateRestaurantOwnerRoleByAdminSchemaResponse,
)


__all__ = [
    # Assign Restaurant Owner
    "AssignRestaurantOwnerByAdminSchemaRequest",
    "AssignRestaurantOwnerByAdminSchemaResponse",
    # Create Restaurant
    "CreateRestaurantByAdminSchemaRequest",
    "CreateRestaurantByAdminSchemaResponse",
    # Delete Restaurant
    "DeleteRestaurantByAdminSchemaRequest",
    # Find Restaurant Owners
    "FindRestaurantOwnersByAdminSchemaItem",
    "FindRestaurantOwnersByAdminSchemaResponse",
    # Transfer Restaurant Ownership
    "TransferRestaurantOwnershipByAdminSchemaResponse",
    # Update Restaurant Owner Role
    "UpdateRestaurantOwnerRoleByAdminSchemaRequest",
    "UpdateRestaurantOwnerRoleByAdminSchemaResponse",
]
