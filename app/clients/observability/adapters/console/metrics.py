"""Console metrics adapter (Adapter).

This module provides a console/print-based implementation for metrics.
This is an ADAPTER in Hexagonal Architecture, useful for development and debugging.

This adapter is framework-agnostic and works with primitive types only.
"""

from typing import Any


class ConsoleMetricsAdapter:
    """Console metrics adapter implementation.

    This adapter implements the MetricsClientPort using console output (print).
    Useful for development and debugging. In production, use adapters like
    Prometheus, DataDog, CloudWatch, etc.

    All operations are non-blocking, safe to use in async contexts, and
    completely framework-agnostic (no dependencies on FastAPI, Flask, etc.).

    Example:
        >>> adapter = ConsoleMetricsAdapter(prefix="[METRICS]")
        >>> await adapter.log_request(
        ...     url="/api/v1/restaurants",
        ...     method="GET",
        ...     status_code=200,
        ...     process_time=0.023,
        ... )
    """

    def __init__(self, prefix: str = "[METRICS]", enabled: bool = True) -> None:
        """Initialize console metrics adapter.

        Args:
            prefix: Prefix to add to all console output
            enabled: Whether logging is enabled (useful for testing)

        Example:
            >>> adapter = ConsoleMetricsAdapter(prefix="[DEV-METRICS]")
        """
        self.prefix = prefix
        self.enabled = enabled

    async def log_request(
        self,
        url: str,
        method: str,
        status_code: int,
        process_time: float,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log an HTTP request with its response and timing information.

        Args:
            url: The request URL path
            method: The HTTP method (GET, POST, etc.)
            status_code: The HTTP response status code
            process_time: The time taken to process the request (in seconds)
            metadata: Optional additional metadata to log
        """
        if not self.enabled:
            return

        # Format metadata if present
        metadata_str = ""
        if metadata:
            metadata_items = [f"{k}={v}" for k, v in metadata.items()]
            metadata_str = f" | {', '.join(metadata_items)}"

        print(
            f"{self.prefix} REQUEST | "
            f"Method: {method} | "
            f"URL: {url} | "
            f"Status: {status_code} | "
            f"Time: {process_time:.4f}s"
            f"{metadata_str}"
        )

    async def log_error(
        self,
        url: str,
        method: str,
        error_type: str,
        error_message: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log an error that occurred during request processing.

        Args:
            url: The request URL path
            method: The HTTP method (GET, POST, etc.)
            error_type: The type/name of the error
            error_message: The error message
            metadata: Optional additional metadata to log
        """
        if not self.enabled:
            return

        # Format metadata if present
        metadata_str = ""
        if metadata:
            metadata_items = [f"{k}={v}" for k, v in metadata.items()]
            metadata_str = f" | {', '.join(metadata_items)}"

        print(
            f"{self.prefix} ERROR | "
            f"Method: {method} | "
            f"URL: {url} | "
            f"Error: {error_type}: {error_message}"
            f"{metadata_str}"
        )

    async def record_metric(
        self,
        metric_name: str,
        value: float,
        **tags: Any,
    ) -> None:
        """Record a custom metric with optional tags.

        Args:
            metric_name: The name of the metric
            value: The metric value
            **tags: Key-value pairs for metric tags/labels
        """
        if not self.enabled:
            return

        # Format tags if present
        tags_str = ""
        if tags:
            tags_items = [f"{k}={v}" for k, v in tags.items()]
            tags_str = f" | Tags: {', '.join(tags_items)}"

        print(f"{self.prefix} METRIC | Name: {metric_name} | Value: {value}{tags_str}")
