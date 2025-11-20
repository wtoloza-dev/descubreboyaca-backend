"""GraphQL API for restaurant domain.

This module provides a GraphQL interface for the restaurant domain,
offering advanced querying capabilities beyond simple REST endpoints.

Features:
- Complex filtering by multiple criteria
- Flexible field selection
- Single endpoint for all restaurant queries
- GraphiQL interface for development
- Dependency injection for clean architecture

Architecture:
    Uses Strawberry's context pattern with FastAPI dependency injection.
    Use cases are injected into the context via FastAPI DI, then accessed
    by resolvers through info.context. This is the standard Strawberry pattern.

    Reference: https://strawberry.rocks/docs/integrations/fastapi

Usage:
    The GraphQL endpoint will be available at /api/v1/restaurants/graphql
    GraphiQL interface at /api/v1/restaurants/graphql (in browser)

Example queries:
    ```graphql
    # Get all restaurants with specific cuisine types
    query {
      restaurants(
        filters: {
          cuisineTypes: [BOYACENSE, COLOMBIANA]
          features: [WIFI, PARKING]
          city: "Tunja"
        }
        pagination: { page: 1, pageSize: 10 }
      ) {
        items {
          id
          name
          description
          cuisineTypes
          features
        }
        total
        totalPages
      }
    }

    # Get a specific restaurant by ID
    query {
      restaurant(id: "01234567890ABCDEFGHIJKLMN") {
        name
        address
        phone
        location {
          latitude
          longitude
        }
      }
    }
    ```
"""

from app.domains.restaurants.presentation.graphql.context import (
    RestaurantGraphQLContext,
    get_graphql_context,
)
from app.domains.restaurants.presentation.graphql.schema import (
    create_graphql_router,
    schema,
)


__all__ = [
    "schema",
    "create_graphql_router",
    "RestaurantGraphQLContext",
    "get_graphql_context",
]
