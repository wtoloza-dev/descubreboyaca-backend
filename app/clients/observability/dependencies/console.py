"""Generic factory for console metrics adapter (app-agnostic).

This module provides a generic factory function for creating console metrics
adapter instances. It accepts configuration as parameters and is app-agnostic.

For app-specific configuration, use app.shared.dependencies.observability module.
"""

from app.clients.observability.adapters.console.metrics import ConsoleMetricsAdapter


def create_console_metrics_adapter(
    prefix: str = "[METRICS]",
    enabled: bool = True,
) -> ConsoleMetricsAdapter:
    """Create a console metrics adapter instance.

    This is a generic factory that accepts configuration as parameters.
    It's app-agnostic and can be used in different contexts.

    Args:
        prefix: Prefix to add to all console output
        enabled: Whether logging is enabled

    Returns:
        ConsoleMetricsAdapter: Configured console metrics adapter instance

    Example:
        >>> adapter = create_console_metrics_adapter(prefix="[DEV]", enabled=True)
    """
    return ConsoleMetricsAdapter(prefix=prefix, enabled=enabled)
