"""Archive domain entities.

This module defines the Archive entities representing a deleted record
stored for historical purposes.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from ulid import ULID


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

    model_config = ConfigDict(from_attributes=True)

    original_table: str
    original_id: str
    data: dict[str, any]
    note: str | None = None


class Archive(ArchiveData):
    """Archive entity with database identity and system metadata.

    Extends ArchiveData with database primary key and system-generated fields.
    The entity generates its own identity (ULID) and timestamps following DDD principles.

    Attributes:
        id: ULID primary key (auto-generated)
        original_table: Name of the source table (inherited)
        original_id: ID from the original record (inherited)
        data: Complete record data as dictionary (inherited)
        note: Optional note or reason for deletion (inherited)
        deleted_at: Timestamp when the record was deleted (auto-generated)
        deleted_by: ID of user who deleted the record (from context)
    """

    id: str = Field(default_factory=lambda: str(ULID()))
    deleted_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    deleted_by: str | None = None
