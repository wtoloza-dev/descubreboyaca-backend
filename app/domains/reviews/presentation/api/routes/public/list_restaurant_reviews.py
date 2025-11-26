"""List restaurant reviews route (Public).

This module provides an endpoint for anyone to view approved reviews of a restaurant.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.reviews.application.use_cases import ListRestaurantReviewsUseCase
from app.domains.reviews.infrastructure.dependencies import (
    get_list_restaurant_reviews_use_case_dependency,
)
from app.domains.reviews.presentation.api.schemas.public import (
    ListRestaurantReviewsSchemaItem,
    ListRestaurantReviewsSchemaResponse,
)
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/restaurants/{restaurant_id}/",
    status_code=status.HTTP_200_OK,
    summary="List restaurant reviews",
    description="Retrieve a paginated list of all approved reviews for a specific restaurant. "
    "This endpoint is public and does not require authentication.",
)
async def handle_list_restaurant_reviews(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    use_case: Annotated[
        ListRestaurantReviewsUseCase,
        Depends(get_list_restaurant_reviews_use_case_dependency),
    ],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
) -> ListRestaurantReviewsSchemaResponse:
    """List all approved reviews for a restaurant.

    This is a public endpoint that returns only approved reviews.
    No authentication is required.

    Args:
        restaurant_id: ULID of the restaurant (validated automatically)
        use_case: List entity reviews use case (injected)
        pagination: Pagination value object with page, page_size, offset, and limit

    Returns:
        ListRestaurantReviewsSchemaResponse: List of approved reviews with pagination

    Raises:
        HTTPException 422: If restaurant_id format is invalid (not a valid ULID)
    """
    reviews, total = await use_case.execute(
        restaurant_id=str(restaurant_id),
        offset=pagination.offset,
        limit=pagination.limit,
        only_approved=True,
    )

    return ListRestaurantReviewsSchemaResponse(
        data=[
            ListRestaurantReviewsSchemaItem.model_validate(review) for review in reviews
        ],
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
