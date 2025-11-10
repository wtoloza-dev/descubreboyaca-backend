"""Admin restaurant schemas package."""

from .assign_owner import AssignOwnerSchemaRequest, OwnershipSchemaResponse
from .create import CreateRestaurantSchemaRequest, CreateRestaurantSchemaResponse
from .delete import DeleteRestaurantSchemaRequest
from .find_owners import FindOwnershipsSchemaResponse
from .remove_owner import RemoveOwnerSchemaResponse
from .transfer_ownership import (
    OwnershipSchemaResponse as TransferOwnershipSchemaResponse,
)
from .update_owner_role import (
    OwnershipSchemaResponse as UpdateOwnerRoleSchemaResponse,
)
from .update_owner_role import (
    UpdateOwnerRoleSchemaRequest,
)


__all__ = [
    # Assign Owner
    "AssignOwnerSchemaRequest",
    # Create
    "CreateRestaurantSchemaRequest",
    "CreateRestaurantSchemaResponse",
    # Delete
    "DeleteRestaurantSchemaRequest",
    # Find Owners
    "FindOwnershipsSchemaResponse",
    # Remove Owner
    "RemoveOwnerSchemaResponse",
    # Transfer Ownership
    "TransferOwnershipSchemaResponse",
    # Update Owner Role
    "UpdateOwnerRoleSchemaRequest",
    "UpdateOwnerRoleSchemaResponse",
    # Common (re-exported)
    "OwnershipSchemaResponse",
]
