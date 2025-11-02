"""Shared domain layer.

This package contains domain primitives and building blocks shared across
multiple bounded contexts: entities, value objects, enums, constants, and patterns.

Note: Archive-related entities have been moved to app/domains/audit/ subdomain.
"""

from .entities import Audit, AuditBasic
from .enums import Perception, SocialMediaPlatform
from .exceptions import (
    AlreadyExistsException,
    DomainException,
    NotFoundException,
    ValidationException,
)
from .factories import generate_ulid, generate_utc_now
from .patterns import AsyncUnitOfWork, UnitOfWorkFactory, UnitOfWorkInterface
from .value_objects import GeoLocation, Pagination, Rating, SocialMedia


__all__ = [
    # Entities
    "Audit",
    "AuditBasic",
    # Enums
    "Perception",
    "SocialMediaPlatform",
    # Exceptions
    "DomainException",
    "NotFoundException",
    "ValidationException",
    "AlreadyExistsException",
    # Factories
    "generate_ulid",
    "generate_utc_now",
    # Patterns
    "AsyncUnitOfWork",
    "UnitOfWorkFactory",
    "UnitOfWorkInterface",
    # Value Objects
    "GeoLocation",
    "Pagination",
    "Rating",
    "SocialMedia",
]
