"""App-specific observability dependencies with concrete configuration.

This module provides FastAPI dependencies for observability clients using
concrete application configuration from settings.

These dependencies are app-specific and use the generic factories from
app.clients.observability.dependencies with concrete configuration values.
"""

from app.clients.observability import create_console_metrics_adapter
from app.core.settings import settings
from app.shared.domain.interfaces import MetricsClientInterface


def get_metrics_client_dependency() -> MetricsClientInterface:
    """Get metrics client instance configured for the application.

    This dependency provides a metrics client using the app's settings.
    Currently uses Console adapter for development, but can be easily
    switched to Prometheus, DataDog, CloudWatch, etc.

    Returns:
        MetricsClientInterface: Configured metrics client instance

    Example:
        >>> @router.post("/items")
        >>> async def create_item(
        ...     metrics_client: MetricsClientInterface = Depends(
        ...         get_metrics_client_dependency
        ...     ),
        ... ):
        ...     await metrics_client.record_metric("items.created", 1.0)
    """
    # TODO: Switch adapter based on settings.ENVIRONMENT or specific config
    # For now, use console adapter with configuration from settings
    return create_console_metrics_adapter(
        prefix=f"[{settings.SCOPE}]",
        enabled=settings.DEBUG,  # Only log in debug mode
    )
