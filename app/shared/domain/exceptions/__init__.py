"""Shared domain exceptions.

Domain exceptions represent business rule violations and error conditions
that are specific to domain logic and shared across multiple bounded contexts.

Base exceptions and common domain errors should be defined here.
"""

from .archive import AlreadyArchivedException
from .base import (
    AlreadyExistsException,
    DomainException,
    NotFoundException,
    ValidationException,
)
from .missing_header import MissingHeaderException


__all__ = [
    "DomainException",
    "NotFoundException",
    "AlreadyExistsException",
    "ValidationException",
    "AlreadyArchivedException",
    "MissingHeaderException",
]
