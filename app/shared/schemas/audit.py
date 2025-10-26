"""Shared audit schemas.

This module contains audit-related schemas (DTOs) for API responses.
These schemas are used by response models to include audit trail information.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditSchema(BaseModel):
    """Audit trail schema for API responses.

    This schema represents audit information in API responses.
    It should be used by response DTOs, not by domain entities.

    Note: This is a schema (DTO), not a domain entity. Domain entities
    should use app.shared.domain.Audit instead.

    Attributes:
        id: ULID identifier
        created_at: Timestamp when the record was created
        updated_at: Timestamp when the record was last updated
        created_by: ULID of the user who created the record
        updated_by: ULID of the user who last updated the record
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique identifier (ULID)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: str | None = Field(None, description="ULID of creator")
    updated_by: str | None = Field(None, description="ULID of last updater")
