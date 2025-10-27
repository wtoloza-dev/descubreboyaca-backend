"""Entity type enumeration for favorites system.

This module defines the types of entities that can be favorited.
"""

from enum import StrEnum


class EntityType(StrEnum):
    """Types of entities that can be favorited.

    This enum defines all the entity types supported by the favorites system.
    Each value represents a different resource type in the application.

    Attributes:
        RESTAURANT: A restaurant entity
        DISH: A dish/menu item entity
        EVENT: An event entity (future feature)
        PLACE: A place/location entity (future feature)
        ACTIVITY: An activity entity (future feature)
    """

    RESTAURANT = "restaurant"
    DISH = "dish"
    EVENT = "event"
    PLACE = "place"
    ACTIVITY = "activity"
