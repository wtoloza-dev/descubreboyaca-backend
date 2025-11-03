"""Shared API schemas.

This package contains shared schemas/DTOs used across multiple domains.
"""

from app.shared.schemas.audit import AuditSchema
from app.shared.schemas.pagination import PaginationSchemaData, PaginationSchemaResponse


__all__ = [
    "AuditSchema",
    "PaginationSchemaData",
    "PaginationSchemaResponse",
]
