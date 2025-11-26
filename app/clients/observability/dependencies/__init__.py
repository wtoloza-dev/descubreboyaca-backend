"""Generic factories for creating observability client instances (app-agnostic).

These factories are generic and don't depend on app-specific configuration.
For app-specific dependencies with concrete configuration, use app.shared.dependencies.
"""

from .console import (
    create_console_metrics_adapter,
)


__all__ = ["create_console_metrics_adapter"]
