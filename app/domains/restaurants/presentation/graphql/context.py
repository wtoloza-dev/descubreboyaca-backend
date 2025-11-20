"""GraphQL context for restaurant domain.

This module defines the custom context class for GraphQL resolvers,
providing access to use cases via FastAPI dependency injection.

Architecture:
    Instead of injecting dependencies directly into resolvers (which Strawberry
    doesn't support), we inject them into the context via FastAPI's DI system.
    This is the standard pattern recommended by Strawberry.

    Benefits:
    - Reuses all existing FastAPI dependencies
    - Use cases are injected once per request
    - Resolvers access them via info.context
    - Clean separation of concerns

    This module also provides the factory function to create the context,
    keeping all context-related logic in one place (high cohesion).
"""

from typing import Annotated

from fastapi import Depends
from strawberry.fastapi import BaseContext

from app.domains.restaurants.application.use_cases.restaurant import (
    FindRestaurantByIdUseCase,
    FindRestaurantsUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_find_restaurant_by_id_use_case_dependency,
    get_find_restaurants_use_case_dependency,
)


class RestaurantGraphQLContext(BaseContext):
    """Custom GraphQL context for restaurant domain.

    This context provides access to use cases that are injected via
    FastAPI's dependency injection system. Each use case is properly
    initialized with its dependencies (repositories, etc.) through DI.

    Attributes:
        find_restaurant_by_id_use_case: Use case for finding a restaurant by ID
        find_restaurants_use_case: Use case for searching restaurants with filters
    """

    def __init__(
        self,
        find_restaurant_by_id_use_case: FindRestaurantByIdUseCase,
        find_restaurants_use_case: FindRestaurantsUseCase,
    ) -> None:
        """Initialize the GraphQL context with injected use cases.

        Args:
            find_restaurant_by_id_use_case: Injected use case for finding by ID
            find_restaurants_use_case: Injected use case for searching
        """
        super().__init__()
        self.find_restaurant_by_id_use_case = find_restaurant_by_id_use_case
        self.find_restaurants_use_case = find_restaurants_use_case


async def get_graphql_context(
    find_restaurant_by_id_use_case: Annotated[
        FindRestaurantByIdUseCase,
        Depends(get_find_restaurant_by_id_use_case_dependency),
    ],
    find_restaurants_use_case: Annotated[
        FindRestaurantsUseCase,
        Depends(get_find_restaurants_use_case_dependency),
    ],
) -> RestaurantGraphQLContext:
    """Create GraphQL context with injected use cases.

    Factory function that uses FastAPI's dependency injection to obtain
    properly configured use cases and creates the GraphQL context.

    This is the standard Strawberry pattern for integrating with FastAPI:
    https://strawberry.rocks/docs/integrations/fastapi

    Args:
        find_restaurant_by_id_use_case: Injected use case for finding by ID
        find_restaurants_use_case: Injected use case for searching

    Returns:
        RestaurantGraphQLContext: Context with injected use cases
    """
    return RestaurantGraphQLContext(
        find_restaurant_by_id_use_case=find_restaurant_by_id_use_case,
        find_restaurants_use_case=find_restaurants_use_case,
    )
