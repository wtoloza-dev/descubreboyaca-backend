"""Pagination dependencies for FastAPI endpoints.

FastAPI dependency that converts user-friendly pagination params
(page, page_size) to database params (offset, limit).
"""

from fastapi import Query

from app.shared.domain import PaginationParams


def get_pagination_params_dependency(
    page: int = Query(default=1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(
        default=20, ge=1, le=100, description="Items per page (max 100)"
    ),
) -> PaginationParams:
    """Convert page/page_size to offset/limit.

    Args:
        page: Page number (1-based)
        page_size: Items per page (1-100)

    Returns:
        PaginationParams with offset and limit

    Example:
        @router.get("/items")
        def list_items(pagination: PaginationParams = Depends(get_pagination_params_dependency)):
            # User: GET /items?page=2&page_size=20
            # Code: pagination.offset=20, pagination.limit=20
            return repo.get_all(offset=pagination.offset, limit=pagination.limit)
    """
    offset = (page - 1) * page_size
    return PaginationParams(offset=offset, limit=page_size)
