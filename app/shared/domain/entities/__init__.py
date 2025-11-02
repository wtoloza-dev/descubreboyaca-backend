"""Shared domain entities.

This package contains domain entities shared across multiple bounded contexts.
Entities are objects with identity and lifecycle.

Note: Archive entities have been moved to app/domains/audit/domain/entities/
"""

from .audit import Audit, AuditBasic, Identity, Timestamp, UserTracking


__all__ = [
    "Audit",
    "AuditBasic",
    "Identity",
    "Timestamp",
    "UserTracking",
]
