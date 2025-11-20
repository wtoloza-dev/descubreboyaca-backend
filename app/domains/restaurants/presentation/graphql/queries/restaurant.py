"""GraphQL queries for Restaurant domain.

This module defines GraphQL query resolvers for the Restaurant entity.

Architecture Note:
    Strawberry GraphQL does not natively support FastAPI's Depends() injection.
    Instead, we use Strawberry's context pattern where dependencies are injected
    into the context via FastAPI, and resolvers access them from info.context.

    This is the standard approach recommended by Strawberry documentation:
    https://strawberry.rocks/docs/integrations/fastapi

    Uses Strawberry's Pydantic integration for automatic type conversion.
"""

import strawberry
from strawberry.types import Info

from app.domains.restaurants.domain.entities import Restaurant
from app.domains.restaurants.presentation.graphql.inputs import (
    PaginationInput,
    RestaurantFilterInput,
)
from app.domains.restaurants.presentation.graphql.types import (
    RestaurantConnection,
    RestaurantType,
)


def convert_restaurant_to_graphql(restaurant: Restaurant) -> RestaurantType:
    """Convert a Restaurant domain entity to a GraphQL type.

    Uses Strawberry's Pydantic integration for automatic conversion.
    Since domain enums are now normalized (ASCII-only names), Strawberry
    can map them directly without manual conversion.

    Args:
        restaurant: Restaurant domain entity

    Returns:
        RestaurantType: GraphQL representation of the restaurant
    """
    return RestaurantType.from_pydantic(restaurant)


def build_filters_dict(filters: RestaurantFilterInput | None) -> dict | None:
    """Build a filters dictionary from GraphQL input.

    Converts GraphQL filter input to the format expected by the use case.

    Args:
        filters: GraphQL filter input

    Returns:
        Dictionary with filters or None if no filters provided
    """
    if not filters:
        return None

    filter_dict = {}

    # Simple text filters
    if filters.city:
        filter_dict["city"] = filters.city
    if filters.state:
        filter_dict["state"] = filters.state
    if filters.country:
        filter_dict["country"] = filters.country

    # Price filters
    if filters.price_level is not None:
        filter_dict["price_level"] = filters.price_level

    # Array filters (converted to lists of values)
    if filters.establishment_types:
        filter_dict["establishment_types"] = [
            et.value for et in filters.establishment_types
        ]
    if filters.cuisine_types:
        filter_dict["cuisine_types"] = [ct.value for ct in filters.cuisine_types]
    if filters.features:
        filter_dict["features"] = [f.value for f in filters.features]
    if filters.tags:
        filter_dict["tags"] = filters.tags

    # Search filter (implemented as name contains)
    if filters.search:
        filter_dict["search"] = filters.search

    return filter_dict if filter_dict else None


@strawberry.type
class RestaurantQuery:
    """GraphQL queries for Restaurant domain.

    Uses dependency injection to obtain use cases, following the same
    pattern as REST endpoints for consistency and maintainability.
    """

    @strawberry.field(description="Get a restaurant by its ID")
    async def restaurant(
        self,
        id: str,
        info: Info,
    ) -> RestaurantType | None:
        """Get a restaurant by ID.

        Args:
            id: Restaurant ID (ULID)
            info: Strawberry context with injected dependencies

        Returns:
            RestaurantType if found, None otherwise
        """
        # Access use case from context (injected via FastAPI DI)
        use_case = info.context.find_restaurant_by_id_use_case
        restaurant = await use_case.execute(id)

        if not restaurant:
            return None

        return convert_restaurant_to_graphql(restaurant)

    @strawberry.field(
        description="Search restaurants with advanced filters and pagination"
    )
    async def restaurants(
        self,
        info: Info,
        filters: RestaurantFilterInput | None = None,
        pagination: PaginationInput | None = None,
    ) -> RestaurantConnection:
        """Search restaurants with advanced filters.

        Supports complex filtering by cuisine types, features, location, price, etc.
        Results are paginated.

        Args:
            info: Strawberry context with injected dependencies
            filters: Optional filters to apply
            pagination: Pagination parameters (defaults to page 1, size 20)

        Returns:
            RestaurantConnection with paginated results
        """
        # Default pagination if not provided
        if pagination is None:
            pagination = PaginationInput(page=1, page_size=20)

        # Validate and cap page_size
        page_size = min(pagination.page_size, 100)
        offset = (pagination.page - 1) * page_size
        limit = page_size

        # Build filters dictionary
        filters_dict = build_filters_dict(filters)

        # Access use case from context (injected via FastAPI DI)
        use_case = info.context.find_restaurants_use_case

        # Execute use case
        restaurants, total = await use_case.execute(
            filters=filters_dict,
            offset=offset,
            limit=limit,
        )

        # Convert to GraphQL types
        items = [convert_restaurant_to_graphql(r) for r in restaurants]

        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size

        return RestaurantConnection(
            items=items,
            total=total,
            page=pagination.page,
            page_size=page_size,
            total_pages=total_pages,
        )
