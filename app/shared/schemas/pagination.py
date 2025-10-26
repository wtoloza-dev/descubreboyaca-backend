"""Generic paginated response schema.

This module provides a generic schema for paginated API responses.
"""

from pydantic import BaseModel, Field


class PaginatedResponse[T](BaseModel):
    """Generic paginated response schema.

    Provides a consistent structure for all paginated endpoints across the API.

    Type Parameters:
        T: Type of items in the response

    Attributes:
        items: List of items in the current page
        page: Current page number (1-based)
        page_size: Number of items per page
        total: Total number of items available

    Example:
        >>> from app.domains.restaurants.schemas import RestaurantListItem
        >>>
        >>> # Define response type
        >>> class RestaurantsListResponse(PaginatedResponse[RestaurantListItem]):
        ...     pass
        >>>
        >>> # Or use directly
        >>> response = PaginatedResponse[RestaurantListItem](
        ...     items=[restaurant1, restaurant2], page=1, page_size=20, total=42
        ... )
    """

    items: list[T] = Field(description="List of items in the current page")
    page: int = Field(ge=1, description="Current page number (1-based)")
    page_size: int = Field(ge=1, le=100, description="Number of items per page")
    total: int = Field(ge=0, description="Total number of items available")
