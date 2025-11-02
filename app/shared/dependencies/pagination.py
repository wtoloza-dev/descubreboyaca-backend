"""Pagination dependencies for FastAPI endpoints.

FastAPI dependency that creates Pagination entity from query parameters.
"""

from fastapi import Query

from app.shared.domain.entities import Pagination


def get_pagination_dependency(
    page: int = Query(default=1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(
        default=20, ge=1, le=100, description="Items per page (max 100)"
    ),
) -> Pagination:
    """Create Pagination entity from query parameters.

    Args:
        page: Page number (1-based)
        page_size: Items per page (1-100)

    Returns:
        Pagination entity with page, page_size, offset, and limit

    Example:
        @router.get("/items")
        def list_items(pagination: Pagination = Depends(get_pagination_dependency)):
            # User: GET /items?page=2&page_size=20
            # Code: pagination.page=2, pagination.page_size=20
            #       pagination.offset=20, pagination.limit=20
            return repo.get_all(offset=pagination.offset, limit=pagination.limit)
    """
    return Pagination(page=page, page_size=page_size)
