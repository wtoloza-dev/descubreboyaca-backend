"""Observability middleware for request/response logging and monitoring.

This module provides middleware for observability features such as logging,
metrics, and tracing. It integrates with the metrics client configured in
the application lifespan.
"""

import asyncio
import time
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.domain.interfaces import MetricsClientInterface


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Middleware for observability features.

    This middleware captures request/response information and delegates
    logging to the metrics client configured in app.state.

    The middleware extracts primitive data (url, method, status_code, etc.)
    and passes it to the framework-agnostic metrics client for processing.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """Process the request and response with observability tracking.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or endpoint handler

        Returns:
            Response: The HTTP response from the application
        """
        # Start timing the request
        start_time = time.perf_counter()

        # Call the next middleware or endpoint
        response = await call_next(request)

        # Calculate processing time in seconds
        process_time = time.perf_counter() - start_time

        # Add processing time header to response (in milliseconds for readability)
        response.headers["X-Process-Time"] = f"{process_time * 1000:.2f}"

        # Get metrics client from app state
        metrics_client: MetricsClientInterface = request.app.state.metrics_client

        # Extract primitive data from request/response
        url = str(request.url.path)
        method = request.method
        status_code = response.status_code

        # Optional: Extract additional metadata
        metadata = {
            "query_params": str(request.url.query) if request.url.query else None,
            "user_agent": request.headers.get("user-agent"),
        }

        # Log request asynchronously without blocking the response
        asyncio.create_task(
            metrics_client.log_request(
                url=url,
                method=method,
                status_code=status_code,
                process_time=process_time,
                metadata=metadata,
            )
        )

        return response
