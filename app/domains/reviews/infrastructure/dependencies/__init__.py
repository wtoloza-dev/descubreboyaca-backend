"""Review domain dependencies.

This module provides async dependency functions for the reviews domain.
"""

from .review import (
    get_review_repository_dependency,
    get_review_service_dependency,
)


__all__ = [
    "get_review_repository_dependency",
    "get_review_service_dependency",
]
