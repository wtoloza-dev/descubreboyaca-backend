"""FastAPI exception handlers for domain exceptions.

This module provides FastAPI-specific exception handlers that convert domain exceptions
into appropriate HTTP responses while maintaining clean separation of concerns.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.shared.domain.exceptions import DomainException

from .mappers import DomainExceptionMapper


logger = logging.getLogger(__name__)


async def domain_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle domain exceptions and convert them to HTTP responses.

    Args:
        request: The FastAPI request object
        exc: The domain exception that was raised

    Returns:
        JSONResponse with appropriate status code and error details
    """
    assert isinstance(exc, DomainException)
    status_code = DomainExceptionMapper.get_status_code(exc)
    error_detail = DomainExceptionMapper.get_error_detail(exc)

    # Log the domain exception
    logger.warning(
        f"Domain exception occurred: {exc.error_code}",
        extra={
            "error_code": exc.error_code,
            "error_message": exc.message,
            "error_context": exc.context,
            "path": str(request.url.path),
            "method": request.method,
        },
    )

    return JSONResponse(status_code=status_code, content=error_detail)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions that are not domain-specific.

    Args:
        request: The FastAPI request object
        exc: The unexpected exception that was raised

    Returns:
        JSONResponse with 500 status and generic error message
    """
    # Log the unexpected exception for debugging
    logger.error(
        f"Unexpected exception occurred: {str(exc)}",
        extra={
            "exception_type": type(exc).__name__,
            "path": str(request.url.path),
            "method": request.method,
        },
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "context": {},
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    # Register domain exception handler
    app.add_exception_handler(DomainException, domain_exception_handler)  # type: ignore[arg-type]

    # Register generic exception handler for unexpected errors
    app.add_exception_handler(Exception, generic_exception_handler)  # type: ignore[arg-type]

    logger.info("Exception handlers registered successfully")
