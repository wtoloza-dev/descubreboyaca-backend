"""Pagination domain entity.

This module defines the pagination entity used across the application.
"""

from pydantic import BaseModel, Field, computed_field


class Pagination(BaseModel):
    """Pagination entity with user-friendly and database-friendly parameters.

    This entity bridges the gap between user-facing pagination (page, page_size)
    and database pagination (offset, limit). It stores both representations to
    avoid repeated calculations.

    Attributes:
        page: Current page number (1-based, user-friendly)
        page_size: Number of items per page (user-friendly)
        offset: Number of records to skip (database-friendly)
        limit: Maximum number of records to return (database-friendly)

    Example:
        >>> pagination = Pagination(page=2, page_size=20)
        >>> pagination.page  # 2
        >>> pagination.page_size  # 20
        >>> pagination.offset  # 20
        >>> pagination.limit  # 20

        >>> # Use in repository
        >>> repo.find(offset=pagination.offset, limit=pagination.limit)

        >>> # Use in response
        >>> response = {"page": pagination.page, "page_size": pagination.page_size}
    """

    page: int = Field(ge=1, description="Page number (1-based)")
    page_size: int = Field(ge=1, le=100, description="Items per page (max 100)")

    @computed_field  # type: ignore[misc]
    @property
    def offset(self) -> int:
        """Calculate offset from page and page_size.

        Returns:
            Number of records to skip for database query

        Example:
            >>> Pagination(page=1, page_size=20).offset  # 0
            >>> Pagination(page=2, page_size=20).offset  # 20
            >>> Pagination(page=3, page_size=10).offset  # 20
        """
        return (self.page - 1) * self.page_size

    @computed_field  # type: ignore[misc]
    @property
    def limit(self) -> int:
        """Get limit (same as page_size).

        This is just an alias for page_size to match database terminology.

        Returns:
            Maximum number of records to return

        Example:
            >>> Pagination(page=1, page_size=20).limit  # 20
        """
        return self.page_size

    model_config = {"frozen": True}
