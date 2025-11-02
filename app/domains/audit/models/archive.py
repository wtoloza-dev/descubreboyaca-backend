"""Archive model for database persistence.

This module defines a generic Archive model to store deleted records from any table.
Records are serialized as JSON to maintain flexibility across different entities.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel

from app.shared.models.audit import ULIDMixin


class ArchiveModel(ULIDMixin, SQLModel, table=True):
    """Archive model for database persistence.

    Stores deleted records from any table as JSON, preserving all data
    and metadata about the deletion.

    Note: Following DDD principles, the ID and timestamps must be provided
    by the Archive domain entity. This model only persists the data.

    Attributes:
        id: ULID primary key (inherited from ULIDMixin, must be provided)
        original_table: Name of the source table
        original_id: ULID from the original record
        data: Complete record data serialized as JSON
        deleted_at: Timestamp when the record was deleted (must be provided)
        deleted_by: ULID of user who deleted the record
        note: Optional note or reason for deletion
    """

    __tablename__ = "archive"

    original_table: str = Field(
        max_length=255,
        index=True,
        description="Name of the source table",
    )
    original_id: str = Field(
        max_length=26,
        index=True,
        description="ULID from the original record",
    )
    data: dict[str, Any] = Field(
        sa_type=JSON,
        description="Complete record data as JSON",
    )
    deleted_at: datetime = Field(
        index=True,
        description="Timestamp when the record was deleted (UTC)",
    )
    deleted_by: str | None = Field(
        default=None,
        max_length=26,
        description="ULID of the user who deleted the record",
    )
    note: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional note or reason for deletion",
    )
