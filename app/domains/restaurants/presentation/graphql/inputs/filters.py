"""GraphQL input types for restaurant filters.

This module defines GraphQL input types for complex restaurant filtering.
"""

import strawberry

from app.domains.restaurants.presentation.graphql.types.enums import (
    CuisineTypeEnum,
    EstablishmentTypeEnum,
    RestaurantFeatureEnum,
)


@strawberry.input(description="Geographic location filter with optional radius")
class GeoLocationFilterInput:
    """Input for filtering by geographic location.

    Allows filtering restaurants within a certain radius of a location.
    """

    latitude: float = strawberry.field(description="Center latitude for search radius")
    longitude: float = strawberry.field(
        description="Center longitude for search radius"
    )
    radius_km: float | None = strawberry.field(
        default=None,
        description="Search radius in kilometers (optional, defaults to 10km)",
    )


@strawberry.input(description="Price level range filter")
class PriceLevelFilterInput:
    """Input for filtering by price level range.

    Allows filtering restaurants within a price range.
    """

    min_price: int | None = strawberry.field(
        default=None,
        description="Minimum price level (1-4)",
    )
    max_price: int | None = strawberry.field(
        default=None,
        description="Maximum price level (1-4)",
    )


@strawberry.input(description="Advanced filters for restaurant queries")
class RestaurantFilterInput:
    """Input for complex restaurant filtering.

    Supports filtering by multiple criteria including location, cuisine types,
    features, price range, and more.

    All filters are optional and can be combined. Multiple values in array
    filters are treated as OR conditions (match any).
    """

    # Text search
    search: str | None = strawberry.field(
        default=None,
        description="Search in name, description, and tags (case-insensitive)",
    )

    # Location filters
    city: str | None = strawberry.field(
        default=None,
        description="Filter by city name (exact match)",
    )
    state: str | None = strawberry.field(
        default=None,
        description="Filter by state/department (exact match)",
    )
    country: str | None = strawberry.field(
        default=None,
        description="Filter by country (exact match)",
    )
    location: GeoLocationFilterInput | None = strawberry.field(
        default=None,
        description="Filter by geographic proximity (requires location coordinates)",
    )

    # Classification filters
    establishment_types: list[EstablishmentTypeEnum] | None = strawberry.field(
        default=None,
        description="Filter by establishment types (restaurant, cafe, etc.) - matches any",
    )
    cuisine_types: list[CuisineTypeEnum] | None = strawberry.field(
        default=None,
        description="Filter by cuisine types - matches any",
    )
    features: list[RestaurantFeatureEnum] | None = strawberry.field(
        default=None,
        description="Filter by features (wifi, parking, etc.) - matches all (AND)",
    )
    tags: list[str] | None = strawberry.field(
        default=None,
        description="Filter by tags - matches any",
    )

    # Price filter
    price_level: int | None = strawberry.field(
        default=None,
        description="Filter by exact price level (1-4)",
    )
    price_range: PriceLevelFilterInput | None = strawberry.field(
        default=None,
        description="Filter by price level range",
    )


@strawberry.input(description="Pagination parameters")
class PaginationInput:
    """Input for pagination parameters."""

    page: int = strawberry.field(
        default=1,
        description="Page number (1-indexed)",
    )
    page_size: int = strawberry.field(
        default=20,
        description="Number of items per page (max 100)",
    )


@strawberry.input(description="Sorting options for restaurant queries")
class RestaurantSortInput:
    """Input for sorting restaurant results."""

    field: str = strawberry.field(
        default="created_at",
        description="Field to sort by (name, created_at, updated_at, price_level)",
    )
    direction: str = strawberry.field(
        default="desc",
        description="Sort direction (asc or desc)",
    )
