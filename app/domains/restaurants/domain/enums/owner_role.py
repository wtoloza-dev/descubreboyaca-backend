"""Restaurant owner role enumeration.

This module defines the roles available for restaurant ownership and management.
These roles determine the level of access and permissions within a restaurant.
"""

from enum import StrEnum


class OwnerRole(StrEnum):
    """Restaurant owner/manager role enumeration.

    Defines the available roles for users who manage or own restaurants.
    Each role has different permissions within the restaurant management system.

    Attributes:
        OWNER: Primary restaurant owner with full management permissions
        MANAGER: Restaurant manager with administrative permissions
        STAFF: Staff member with limited management permissions
    """

    OWNER = "owner"
    MANAGER = "manager"
    STAFF = "staff"

