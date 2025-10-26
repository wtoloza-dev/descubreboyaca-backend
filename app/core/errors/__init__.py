"""Infrastructure error handling module.

This module provides FastAPI-specific error handling, including exception handlers
and mappers that convert domain exceptions to appropriate HTTP responses.
"""

from .handlers import register_exception_handlers as register_exception_handlers
from .mappers import DomainExceptionMapper


__all__ = [
    "register_exception_handlers",
    "DomainExceptionMapper",
]
