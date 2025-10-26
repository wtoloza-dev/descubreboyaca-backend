"""Restaurant owner relationship model.

This module defines the many-to-many relationship between restaurants and their owners.
A restaurant can have multiple owners/managers, and a user can own multiple restaurants.
"""

from sqlmodel import Field, SQLModel

from app.shared.models import TimestampMixin, UserTrackingMixin


class RestaurantOwnerModel(TimestampMixin, UserTrackingMixin, SQLModel, table=True):
    """Restaurant ownership relationship model.

    This model represents the many-to-many relationship between restaurants
    and their owners/managers. It tracks who can manage each restaurant and
    with what level of permissions.

    Note: This model uses TimestampMixin and UserTrackingMixin for complete audit
    tracking without requiring a ULID primary key (uses composite PK instead).

    Attributes:
        restaurant_id: Foreign key to restaurants table (part of composite PK)
        owner_id: Foreign key to users table (part of composite PK)
        role: Role of the user in restaurant management (owner, manager, staff)
        is_primary: Whether this is the primary owner (only one per restaurant)
        created_at: Timestamp when ownership was assigned (inherited from TimestampMixin)
        updated_at: Timestamp when ownership was last updated (inherited from TimestampMixin)
        created_by: ULID of the admin who assigned this ownership (inherited from UserTrackingMixin)
        updated_by: ULID of the admin who last modified this ownership (inherited from UserTrackingMixin)
    """

    __tablename__ = "restaurant_owners"

    restaurant_id: str = Field(
        foreign_key="restaurants.id",
        primary_key=True,
        max_length=26,
        description="ULID of the restaurant",
    )
    owner_id: str = Field(
        foreign_key="users.id",
        primary_key=True,
        max_length=26,
        description="ULID of the owner/manager user",
    )
    role: str = Field(
        default="owner",
        max_length=50,
        nullable=False,
        description="Role in restaurant management (owner, manager, staff)",
    )
    is_primary: bool = Field(
        default=False,
        nullable=False,
        description="Whether this is the primary owner of the restaurant",
    )
