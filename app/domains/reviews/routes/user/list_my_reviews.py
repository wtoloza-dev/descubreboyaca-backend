"""List user reviews route.

This module provides an endpoint for users to list their own reviews.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

# Auth
from app.domains.auth.dependencies import get_current_user_dependency
from app.domains.auth.domain import User

# Reviews
from app.domains.reviews.dependencies import get_review_service_dependency
from app.domains.reviews.schemas import (
    ListMyReviewsSchemaItem,
    ListMyReviewsSchemaResponse,
)
from app.domains.reviews.services import ReviewService

# Shared
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination


router = APIRouter()


@router.get(
    path="/me/",
    status_code=status.HTTP_200_OK,
    summary="List my reviews",
    description="Retrieve a paginated list of all reviews created by the authenticated user. "
    "Results can be filtered by status (pending, approved, rejected).",
)
async def handle_list_my_reviews(
    current_user: Annotated[User, Depends(get_current_user_dependency)],
    service: Annotated[ReviewService, Depends(get_review_service_dependency)],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
) -> ListMyReviewsSchemaResponse:
    """List my reviews.

    Args:
        current_user: Authenticated user from JWT token
        service: Review service (injected)
        pagination: Pagination value object with page, page_size, offset, and limit

    Returns:
        ListMyReviewsSchemaResponse: List of reviews
    """
    reviews, total = await service.list_user_reviews(
        user_id=current_user.id,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    return ListMyReviewsSchemaResponse(
        items=[ListMyReviewsSchemaItem.model_validate(review) for review in reviews],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total,
    )
