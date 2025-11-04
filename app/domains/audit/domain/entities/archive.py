"""Archive domain entities following DDD principles.

This module defines the Archive entities representing a deleted record
stored for historical purposes.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain.entities.audit import Identity


class ArchiveData(BaseModel):
    """Archive data fields for archiving records.

    Contains only the core business data needed to archive a record,
    without system-generated metadata.

    Attributes:
        original_table: Name of the source table
        original_id: ID from the original record
        data: Complete record data as dictionary
        note: Optional note or reason for deletion
    """

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    original_table: str
    original_id: str
    data: dict[str, Any]
    note: str | None = None


class Archive(ArchiveData, Identity):
    """Archive entity with database identity and deletion metadata.

    Extends ArchiveData with database primary key and deletion tracking fields.
    The entity generates its own identity (ULID) and deletion timestamp following DDD principles.

    Note: Uses Identity (not full Audit/Timestamp) because archived records
    use deleted_at/deleted_by instead of created_at/updated_at/created_by/updated_by.

    Attributes:
        id: ULID primary key (auto-generated, inherited from Identity)
        deleted_at: Timestamp when the record was deleted (auto-generated)
        deleted_by: ULID of user who deleted the record
        original_table: Name of the source table (inherited from ArchiveData)
        original_id: ID from the original record (inherited from ArchiveData)
        data: Complete record data as dictionary (inherited from ArchiveData)
        note: Optional note or reason for deletion (inherited from ArchiveData)
    """

    deleted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    deleted_by: str | None = None
