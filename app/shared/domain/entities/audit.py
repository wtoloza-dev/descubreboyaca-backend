"""Audit domain entities.

This module defines base audit entities that other domain entities can inherit from.
Each entity corresponds 1:1 with a mixin in the models layer.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain.factories import generate_ulid, generate_utc_now


class Identity(BaseModel):
    """Identity entity with ULID-based primary key.

    Corresponds to: ULIDMixin (models layer)

    Base entity for domain objects that require a unique identifier.
    The entity generates its own identity (ULID) following DDD principles.

    Attributes:
        id: ULID primary key (auto-generated)
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=generate_ulid)


class Timestamp(BaseModel):
    """Timestamp entity with creation and update timestamps.

    Corresponds to: TimestampMixin (models layer)

    Base entity for domain objects that require timestamp tracking.
    All timestamps are automatically generated in UTC.

    Attributes:
        created_at: Timestamp when the record was created (auto-generated)
        updated_at: Timestamp when the record was last updated (auto-generated)
    """

    model_config = ConfigDict(from_attributes=True)

    created_at: datetime = Field(default_factory=generate_utc_now)
    updated_at: datetime = Field(default_factory=generate_utc_now)


class UserTracking(BaseModel):
    """User tracking entity with creator and updater information.

    Corresponds to: UserTrackingMixin (models layer)

    Base entity for domain objects that require user tracking capabilities.
    Tracks which user created and last modified a record.

    Attributes:
        created_by: ULID of the user who created the record
        updated_by: ULID of the user who last updated the record
    """

    model_config = ConfigDict(from_attributes=True)

    created_by: str | None = None
    updated_by: str | None = None


class AuditBasic(Identity, Timestamp):
    """Basic audit entity with identity and timestamps.

    Corresponds to: Identity (ULIDMixin) + Timestamp (TimestampMixin) in models layer

    Base entity for domain objects that require identity and timestamp tracking,
    but don't need user tracking (created_by/updated_by).

    This is useful for entities like reviews, favorites, and other user-generated
    content where the user relationship is explicit through a foreign key.

    Attributes:
        id: ULID primary key (inherited from Identity)
        created_at: Timestamp when the record was created (inherited from Timestamp)
        updated_at: Timestamp when the record was last updated (inherited from Timestamp)
    """

    model_config = ConfigDict(from_attributes=True)


class Audit(Identity, Timestamp, UserTracking):
    """Audit entity with full audit trail and database identity.

    Corresponds to: AuditMixin (models layer)

    Base entity for domain objects that require complete audit tracking.
    Combines Identity, Timestamp, and UserTracking entities to provide
    a complete audit trail following DDD principles.

    Attributes:
        id: ULID primary key (inherited from Identity)
        created_at: Timestamp when the record was created (inherited from Timestamp)
        updated_at: Timestamp when the record was last updated (inherited from Timestamp)
        created_by: ULID of the user who created the record (inherited from UserTracking)
        updated_by: ULID of the user who last updated the record (inherited from UserTracking)
    """

    model_config = ConfigDict(from_attributes=True)
