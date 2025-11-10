"""Restaurant filters dependencies.

This module provides FastAPI dependency functions for handling restaurant filters
using Pydantic models to validate and clean query parameters.
"""

from fastapi import Query
from pydantic import BaseModel, Field


class RestaurantFilters(BaseModel):
    """Restaurant filter parameters for query operations.

    This model defines the available filters for restaurant queries.
    All fields are optional. Only non-None values will be used in the query.

    Note: Only direct/simple filters are supported. For complex filtering
    (arrays, tags, multiple criteria), consider using GraphQL.

    Attributes:
        city: Filter by city name
        state: Filter by state/department name
        country: Filter by country name
        price_level: Filter by price range (1-4)
    """

    city: str | None = Field(
        default=None,
        description="Filter restaurants by city name",
        examples=["Tunja", "Duitama", "Sogamoso"],
    )
    state: str | None = Field(
        default=None,
        description="Filter restaurants by state/department",
        examples=["Boyacá"],
    )
    country: str | None = Field(
        default=None,
        description="Filter restaurants by country",
        examples=["Colombia"],
    )
    price_level: int | None = Field(
        default=None,
        ge=1,
        le=4,
        description="Filter by price range: 1=budget, 2=moderate, 3=expensive, 4=luxury",
        examples=[1, 2, 3, 4],
    )


def get_restaurant_filters_dependency(
    city: str | None = Query(
        default=None,
        description="Filter restaurants by city name",
        examples=["Tunja", "Duitama", "Sogamoso"],
    ),
    state: str | None = Query(
        default=None,
        description="Filter restaurants by state/department",
        examples=["Boyacá"],
    ),
    country: str | None = Query(
        default=None,
        description="Filter restaurants by country",
        examples=["Colombia"],
    ),
    price_level: int | None = Query(
        default=None,
        ge=1,
        le=4,
        description="Filter by price range: 1=budget, 2=moderate, 3=expensive, 4=luxury",
        examples=[1, 2, 3, 4],
    ),
) -> RestaurantFilters:
    """FastAPI dependency to get restaurant filters from query parameters.

    This dependency extracts filter parameters from the request query string,
    validates them using Pydantic, and returns a RestaurantFilters object.

    Note: Only direct/simple filters are supported. For complex filtering
    (arrays, tags, multiple criteria), consider using GraphQL.

    Args:
        city: Optional city filter
        state: Optional state/department filter
        country: Optional country filter
        price_level: Optional price range filter (1-4)

    Returns:
        RestaurantFilters: Validated filter parameters

    Example:
        >>> # In a FastAPI route:
        >>> @router.get("/restaurants")
        >>> async def list_restaurants(
        ...     filters: RestaurantFilters = Depends(get_restaurant_filters_dependency),
        ... ):
        ...     filter_dict = filters.model_dump(exclude_none=True)
        ...     restaurants = await repo.find(filters=filter_dict or None)
    """
    return RestaurantFilters(
        city=city,
        state=state,
        country=country,
        price_level=price_level,
    )
