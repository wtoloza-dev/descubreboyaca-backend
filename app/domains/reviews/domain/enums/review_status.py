"""Review status enumeration.

This module defines the status of a review in the moderation workflow.
"""

from enum import StrEnum


class ReviewStatus(StrEnum):
    """Review status enumeration.

    Defines the moderation status of a review.

    Attributes:
        PENDING: Review is awaiting moderation
        APPROVED: Review has been approved and is publicly visible
        REJECTED: Review has been rejected and is not visible
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
