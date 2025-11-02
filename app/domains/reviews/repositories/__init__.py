"""Reviews repositories.

This module contains all repository implementations for the reviews domain.
"""

from .review import ReviewRepositoryPostgreSQL, ReviewRepositorySQLite


__all__ = [
    "ReviewRepositoryPostgreSQL",
    "ReviewRepositorySQLite",
]
