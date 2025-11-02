"""Shared domain exceptions.

Domain exceptions represent business rule violations and error conditions
that are specific to domain logic and shared across multiple bounded contexts.

Base exceptions and common domain errors should be defined here.
"""

from .already_exists import AlreadyExistsException
from .domain_exception import DomainException
from .forbidden import ForbiddenException
from .missing_header import MissingHeaderException
from .not_found import NotFoundException
from .unauthorized import UnauthorizedException
from .validation import ValidationException


__all__ = [
    "DomainException",
    "NotFoundException",
    "AlreadyExistsException",
    "ValidationException",
    "ForbiddenException",
    "UnauthorizedException",
    "MissingHeaderException",
]
