"""Pagination domain value object.

This module defines the pagination value object used across the application.
Value objects are immutable objects that represent descriptive aspects of the domain.
"""

from pydantic import BaseModel, ConfigDict, Field, computed_field


class Pagination(BaseModel):
    """Pagination value object with user-friendly and database-friendly parameters.

    Immutable value object bridging the gap between user-facing pagination (page, page_size)
    and database pagination (offset, limit). It stores both representations to
    avoid repeated calculations.

    As a value object, it has no identity and is immutable (frozen).

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

    model_config = ConfigDict(frozen=True)

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
