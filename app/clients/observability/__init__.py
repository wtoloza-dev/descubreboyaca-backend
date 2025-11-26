"""Observability and metrics clients (Hexagonal Architecture - Ports and Adapters).

This package implements the Ports and Adapters pattern for observability clients
following best practices for metrics, logging, and monitoring.

Structure:
- ports/: PORTS (Port definitions) - defines the contracts
  - metrics.py: Metrics client port

- adapters/: ADAPTERS (Implementations) - concrete implementations
  - console/: Console/Print adapter (for development)
    - metrics.py: Console metrics adapter

- dependencies/: GENERIC FACTORIES (app-agnostic) - creates adapter instances
  - console.py: Generic console adapter factories that accept config as parameters

For app-specific dependencies with concrete configuration, use app.shared.dependencies:

Usage:
    >>> from app.shared.dependencies import get_metrics_client_dependency
    >>> from fastapi import Depends
    >>>
    >>> async def log_request(
    ...     metrics_client=Depends(get_metrics_client_dependency),
    ... ):
    ...     await metrics_client.log_request(...)
"""

from app.clients.observability.adapters import ConsoleMetricsAdapter
from app.clients.observability.dependencies import create_console_metrics_adapter
from app.clients.observability.ports import MetricsClientPort


__all__ = [
    # Ports (Contracts)
    "MetricsClientPort",
    # Adapters (Implementations)
    "ConsoleMetricsAdapter",
    # Generic Factories (app-agnostic)
    "create_console_metrics_adapter",
]
