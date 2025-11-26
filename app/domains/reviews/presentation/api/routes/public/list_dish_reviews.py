"""List dish reviews route (Public).

This module provides an endpoint for anyone to view approved reviews of a dish.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.reviews.application.use_cases import ListDishReviewsUseCase
from app.domains.reviews.infrastructure.dependencies import (
    get_list_dish_reviews_use_case_dependency,
)
from app.domains.reviews.presentation.api.schemas.public import (
    ListDishReviewsSchemaItem,
    ListDishReviewsSchemaResponse,
)
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/dishes/{dish_id}/",
    status_code=status.HTTP_200_OK,
    summary="List dish reviews",
    description="Retrieve a paginated list of all approved reviews for a specific dish. "
    "This endpoint is public and does not require authentication.",
)
async def handle_list_dish_reviews(
    dish_id: Annotated[
        ULID,
        Path(
            description="ULID of the dish",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    use_case: Annotated[
        ListDishReviewsUseCase,
        Depends(get_list_dish_reviews_use_case_dependency),
    ],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
) -> ListDishReviewsSchemaResponse:
    """List all approved reviews for a dish.

    This is a public endpoint that returns only approved reviews.
    No authentication is required.

    Args:
        dish_id: ULID of the dish (validated automatically)
        use_case: List entity reviews use case (injected)
        pagination: Pagination value object with page, page_size, offset, and limit

    Returns:
        ListDishReviewsSchemaResponse: List of approved reviews with pagination

    Raises:
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    reviews, total = await use_case.execute(
        dish_id=str(dish_id),
        offset=pagination.offset,
        limit=pagination.limit,
        only_approved=True,
    )

    return ListDishReviewsSchemaResponse(
        data=[ListDishReviewsSchemaItem.model_validate(review) for review in reviews],
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
