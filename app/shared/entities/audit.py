"""Audit domain entities.

This module defines base audit entities that other domain entities can inherit from.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from ulid import ULID


class Audit(BaseModel):
    """Audit entity with full audit trail and database identity.

    Base entity for domain objects that require complete audit tracking.
    The entity generates its own identity (ULID) and timestamps following DDD principles.
    All entities that inherit from Audit will have identity and metadata.

    Attributes:
        id: ULID primary key (auto-generated)
        created_at: Timestamp when the record was created (auto-generated)
        updated_at: Timestamp when the record was last updated (auto-generated)
        created_by: ULID of the user who created the record
        updated_by: ULID of the user who last updated the record
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=lambda: str(ULID()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    created_by: str | None = None
    updated_by: str | None = None
