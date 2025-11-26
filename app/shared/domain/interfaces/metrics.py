"""Metrics client interface.

This module re-exports the metrics client port from app.clients.observability
with a domain-friendly alias name.

The actual interface definition (source of truth) is in app.clients.observability.ports.metrics
This module just provides an alias for domain layer usage.
"""

from app.clients.observability.ports import MetricsClientPort


# Alias for domain layer nomenclature
MetricsClientInterface = MetricsClientPort
