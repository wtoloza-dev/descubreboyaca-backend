"""Shared domain interfaces.

This package contains abstract interfaces and protocols shared across multiple domains,
defining contracts for repositories, services, and clients.

Note: Archive repository interfaces have been moved to app/domains/audit/domain/interfaces/
"""

from app.shared.domain.interfaces.metrics import MetricsClientInterface


__all__ = ["MetricsClientInterface"]
