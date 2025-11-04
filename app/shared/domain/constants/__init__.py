"""Shared constants.

This package contains constants shared across multiple bounded contexts.
Constants represent fixed values used throughout the application.
"""

from .audit import AUDIT_FIELDS_EXCLUDE
from .defaults import (
    DEFAULT_COUNTRY,
    DEFAULT_CURRENCY,
    DEFAULT_PAGE_SIZE,
    DEFAULT_STATE,
    DUITAMA_COORDINATES,
    MAX_ADDRESS_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
    MAX_NOTE_LENGTH,
    MAX_PAGE_SIZE,
    PAIPA_COORDINATES,
    SOGAMOSO_COORDINATES,
    TUNJA_COORDINATES,
    VILLA_DE_LEYVA_COORDINATES,
)


__all__ = [
    "DEFAULT_COUNTRY",
    "DEFAULT_STATE",
    "DEFAULT_CURRENCY",
    "TUNJA_COORDINATES",
    "DUITAMA_COORDINATES",
    "SOGAMOSO_COORDINATES",
    "PAIPA_COORDINATES",
    "VILLA_DE_LEYVA_COORDINATES",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "MAX_NAME_LENGTH",
    "MAX_DESCRIPTION_LENGTH",
    "MAX_ADDRESS_LENGTH",
    "MAX_NOTE_LENGTH",
    # Audit
    "AUDIT_FIELDS_EXCLUDE",
]
