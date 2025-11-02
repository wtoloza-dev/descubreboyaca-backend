"""Entity type enumeration.

This module defines the types of entities that can be reviewed.
"""

from enum import StrEnum


class EntityType(StrEnum):
    """Entity type enumeration.

    Defines the types of entities that can receive reviews in the platform.
    This is designed to be extensible - new entity types can be added
    without database schema changes.

    Attributes:
        RESTAURANT: Restaurant entities
        EVENT: Event entities
        PLACE: Tourist place/attraction entities
        ACTIVITY: Activity entities
    """

    RESTAURANT = "restaurant"
    EVENT = "event"
    PLACE = "place"
    ACTIVITY = "activity"
