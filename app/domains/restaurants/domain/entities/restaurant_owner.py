"""Restaurant owner domain entities following DDD principles.

This module defines the RestaurantOwner domain entities following DDD principles.
These entities represent the ownership relationship between users and restaurants.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain.entities import Timestamp, UserTracking


class RestaurantOwnerData(BaseModel):
    """Restaurant owner data fields without system metadata.

    Contains only the core business data needed to assign an owner to a restaurant,
    without system-generated metadata like timestamps.

    Attributes:
        restaurant_id: ULID of the restaurant being owned
        owner_id: ULID of the user who owns/manages the restaurant
        role: Role of the owner in restaurant management (owner, manager, staff)
        is_primary: Whether this is the primary owner of the restaurant
    """

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    restaurant_id: str = Field(..., min_length=26, max_length=26)
    owner_id: str = Field(..., min_length=26, max_length=26)
    role: str = Field(default="owner", max_length=50)
    is_primary: bool = Field(default=False)


class RestaurantOwner(RestaurantOwnerData, Timestamp, UserTracking):
    """Restaurant owner entity with audit trail.

    Extends RestaurantOwnerData with timestamp and user tracking fields.
    This represents the complete ownership relationship with full audit trail.

    Note: This entity does not have a separate ULID id field because it uses
    a composite primary key (restaurant_id, owner_id). Therefore, it inherits
    from Timestamp and UserTracking instead of full Audit.

    Attributes:
        restaurant_id: ULID of the restaurant (inherited from RestaurantOwnerData, part of composite PK)
        owner_id: ULID of the user (inherited from RestaurantOwnerData, part of composite PK)
        role: Role in restaurant management (inherited from RestaurantOwnerData)
        is_primary: Whether this is the primary owner (inherited from RestaurantOwnerData)
        created_at: Timestamp when ownership was assigned (inherited from Timestamp)
        updated_at: Timestamp when ownership was last modified (inherited from Timestamp)
        created_by: ULID of the admin who assigned this ownership (inherited from UserTracking)
        updated_by: ULID of the admin who last modified this ownership (inherited from UserTracking)
    """
