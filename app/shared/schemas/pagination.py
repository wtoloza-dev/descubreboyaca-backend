"""Generic paginated response schema.

This module provides a generic schema for paginated API responses.
"""

from pydantic import BaseModel, Field


class PaginationSchemaData(BaseModel):
    """Pagination metadata schema.

    Contains metadata about pagination state and totals.

    Attributes:
        page: Current page number (1-based)
        page_size: Number of items per page
        total: Total number of items available
    """

    page: int = Field(ge=1, description="Current page number (1-based)")
    page_size: int = Field(ge=1, le=100, description="Number of items per page")
    total: int = Field(ge=0, description="Total number of items available")


class PaginationSchemaResponse[T](BaseModel):
    """Generic paginated response schema.

    Provides a consistent structure for all paginated endpoints across the API.
    Concrete implementations should inherit from this class and define both
    data and pagination fields.

    Type Parameters:
        T: Type of items in the response

    Attributes:
        data: List of items in the current page
        pagination: Pagination metadata

    Example:
        >>> from app.domains.restaurants.schemas import RestaurantListItem
        >>>
        >>> # Define response type
        >>> class FindAllRestaurantSchemaResponse(
        ...     PaginationSchemaResponse[RestaurantListItem]
        ... ):
        ...     data: list[RestaurantListItem] = Field(
        ...         description="List of restaurants"
        ...     )
        ...     pagination: PaginationSchemaData = Field(
        ...         description="Pagination metadata"
        ...     )
    """

    data: list[T] = Field(description="List of items in the current page")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
