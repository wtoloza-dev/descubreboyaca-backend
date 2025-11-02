"""Reviews domain exceptions.

This module contains all domain-specific exceptions for the reviews domain.
"""

from app.domains.reviews.domain.exceptions.duplicate_review import (
    DuplicateReviewException,
)
from app.domains.reviews.domain.exceptions.entity_not_found import (
    EntityNotFoundException,
)
from app.domains.reviews.domain.exceptions.invalid_rating import InvalidRatingException
from app.domains.reviews.domain.exceptions.review_not_found import (
    ReviewNotFoundException,
)
from app.domains.reviews.domain.exceptions.unauthorized_review import (
    UnauthorizedReviewException,
)


__all__ = [
    "DuplicateReviewException",
    "EntityNotFoundException",
    "InvalidRatingException",
    "ReviewNotFoundException",
    "UnauthorizedReviewException",
]
