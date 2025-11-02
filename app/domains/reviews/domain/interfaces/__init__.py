"""Reviews domain interfaces.

This module contains all domain interfaces (protocols) for the reviews domain.
"""

from app.domains.reviews.domain.interfaces.review_repository import (
    ReviewRepositoryInterface,
)


__all__ = [
    "ReviewRepositoryInterface",
]
