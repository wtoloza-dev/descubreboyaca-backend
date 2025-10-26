"""Domain factories for generating domain objects and identifiers.

This package provides factory functions for creating domain-level identifiers,
timestamps, and other value objects that are used across multiple entities.
"""

from .datetime import generate_utc_now
from .ulid import generate_ulid


__all__ = [
    "generate_ulid",
    "generate_utc_now",
]
