"""Restaurant database model.

This module defines the Restaurant ORM model for database operations.
"""

from sqlmodel import Field, SQLModel

from app.shared.models import AuditMixin


class RestaurantModel(AuditMixin, SQLModel, table=True):
    """Restaurant database model.

    Represents a restaurant entity in the database with full audit trail.
    Inherits ULID-based id, timestamp and user tracking fields from AuditMixin.

    When a restaurant is deleted, it's archived in the 'archive' table
    and removed from this table.

    Attributes:
        id: ULID primary key (inherited from AuditMixin)
        name: Restaurant name
        description: Optional description
        address: Restaurant address
        phone: Contact phone number
        email: Contact email
        created_at: Timestamp when created (inherited from AuditMixin)
        updated_at: Timestamp when updated (inherited from AuditMixin)
        created_by: ULID of creator (inherited from AuditMixin)
        updated_by: ULID of last updater (inherited from AuditMixin)
    """

    __tablename__ = "restaurants"

    name: str = Field(max_length=255, nullable=False, index=True)
    description: str | None = Field(default=None, max_length=1000)
    address: str = Field(max_length=500, nullable=False)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=255)
