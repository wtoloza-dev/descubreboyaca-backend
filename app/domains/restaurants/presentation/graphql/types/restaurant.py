"""GraphQL types for Restaurant domain.

This module defines GraphQL types for the Restaurant entity.
Uses Strawberry's Pydantic integration to automatically generate types from domain models.
"""

import strawberry

from app.domains.restaurants.domain.entities import Restaurant


@strawberry.experimental.pydantic.type(
    model=Restaurant,
    all_fields=True,
    description="Restaurant entity with complete information",
)
class RestaurantType:
    """GraphQL type for Restaurant entity.

    Automatically generated from the Restaurant Pydantic model using all_fields=True.
    Domain enums are now normalized (ASCII-only names) so Strawberry can map them
    automatically without manual conversion.

    All fields including enums, value objects, and scalars are auto-generated,
    ensuring perfect synchronization between domain and GraphQL schema.
    """

    pass


@strawberry.type(description="Paginated list of restaurants")
class RestaurantConnection:
    """GraphQL type for paginated restaurant results.

    Follows the Relay connection pattern for pagination.
    """

    items: list[RestaurantType] = strawberry.field(
        description="List of restaurants in current page"
    )
    total: int = strawberry.field(
        description="Total number of restaurants matching the query"
    )
    page: int = strawberry.field(description="Current page number")
    page_size: int = strawberry.field(description="Number of items per page")
    total_pages: int = strawberry.field(description="Total number of pages")
