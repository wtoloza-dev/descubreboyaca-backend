"""Shared domain layer.

This package contains domain primitives and building blocks shared across
multiple bounded contexts: entities, value objects, enums, constants, and patterns.
"""

from .entities import Archive, ArchiveData, Audit, AuditBasic
from .enums import Perception, SocialMediaPlatform
from .exceptions import (
    AlreadyArchivedException,
    AlreadyExistsException,
    DomainException,
    NotFoundException,
    ValidationException,
)
from .factories import generate_ulid, generate_utc_now
from .interfaces import (
    ArchiveRepositoryInterface,
    AsyncArchiveRepositoryInterface,
)
from .patterns import AsyncUnitOfWork, UnitOfWorkFactory, UnitOfWorkInterface
from .value_objects import GeoLocation, Rating, SocialMedia


__all__ = [
    # Entities
    "Archive",
    "ArchiveData",
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
    "AlreadyArchivedException",
    # Factories
    "generate_ulid",
    "generate_utc_now",
    # Interfaces
    "ArchiveRepositoryInterface",
    "AsyncArchiveRepositoryInterface",
    # Patterns
    "AsyncUnitOfWork",
    "UnitOfWorkFactory",
    "UnitOfWorkInterface",
    # Value Objects
    "GeoLocation",
    "Rating",
    "SocialMedia",
]
