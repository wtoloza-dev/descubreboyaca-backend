"""Metrics client port (Port).

This module defines the Port interface for observability and metrics clients.
This is a PORT in Hexagonal Architecture (Clean Architecture).

Best Practices:
    - Client instances can be initialized once on startup
    - Operations should be non-blocking (async)
    - Failures should not affect main application flow
    - Framework-agnostic: uses primitive types, not framework-specific objects
"""

from typing import Any, Protocol


class MetricsClientPort(Protocol):
    """Port defining the contract for observability and metrics clients.

    This is the PORT in Hexagonal Architecture. Any metrics client implementation
    (Console, Prometheus, DataDog, CloudWatch, etc.) must implement this interface.

    The client provides methods for logging requests, errors, and custom metrics.
    All operations should be asynchronous, non-blocking, and framework-agnostic.
    """

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

        Example:
            >>> await client.log_request(
            ...     url="/api/v1/restaurants",
            ...     method="GET",
            ...     status_code=200,
            ...     process_time=0.023,
            ...     metadata={"user_id": "123", "query_params": "limit=10"},
            ... )
        """
        ...

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

        Example:
            >>> await client.log_error(
            ...     url="/api/v1/restaurants",
            ...     method="POST",
            ...     error_type="ValidationError",
            ...     error_message="Invalid input data",
            ...     metadata={"user_id": "123"},
            ... )
        """
        ...

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

        Example:
            >>> await client.record_metric(
            ...     "database.query.duration",
            ...     0.045,
            ...     table="restaurants",
            ...     operation="select",
            ... )
        """
        ...
