"""Audit and timestamp base models for database entities.

This module provides mixin classes for adding audit fields (created_at, updated_at,
created_by, updated_by) and ULID-based primary keys to SQLModel tables.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel
from ulid import ULID


class ULIDMixin(SQLModel):
    """Mixin that adds a ULID-based primary key to a model.

    ULID (Universally Unique Lexicographically Sortable Identifier) provides
    better performance and ordering compared to traditional UUIDs.

    Attributes:
        id: ULID primary key stored as string
    """

    id: str = Field(
        default_factory=lambda: str(ULID()),
        primary_key=True,
        max_length=26,
        description="ULID primary key",
    )


class TimestampMixin(SQLModel):
    """Mixin that adds timestamp fields to a model.

    This mixin provides automatic timestamp tracking for entity creation
    and updates. All timestamps are stored in UTC.

    Attributes:
        created_at: Timestamp when the record was created
        updated_at: Timestamp when the record was last updated
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(datetime.UTC),
        nullable=False,
        description="Timestamp when the record was created (UTC)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(datetime.UTC),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(datetime.UTC)},
        description="Timestamp when the record was last updated (UTC)",
    )


class AuditMixin(ULIDMixin, TimestampMixin):
    """Mixin that adds full audit fields to a model.

    This mixin combines ULIDMixin and TimestampMixin with user tracking fields
    to maintain a complete audit trail of who created and modified records.

    Attributes:
        id: ULID primary key (inherited from ULIDMixin)
        created_at: Timestamp when the record was created (inherited from TimestampMixin)
        updated_at: Timestamp when the record was last updated (inherited from TimestampMixin)
        created_by: ULID of the user who created the record
        updated_by: ULID of the user who last updated the record
    """

    created_by: str | None = Field(
        default=None,
        nullable=True,
        max_length=26,
        description="ULID of the user who created the record",
    )
    updated_by: str | None = Field(
        default=None,
        nullable=True,
        max_length=26,
        description="ULID of the user who last updated the record",
    )
