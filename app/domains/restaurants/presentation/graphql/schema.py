"""GraphQL schema for restaurant domain.

This module defines the main GraphQL schema that combines all queries and mutations.

Architecture:
    - Configures scalar overrides for Pydantic types (HttpUrl, Decimal)
    - Assembles the complete schema from queries
    - Creates the GraphQL router with context injection

    Context creation is delegated to context.py for better cohesion.
"""

from decimal import Decimal
from typing import NewType

import strawberry
from pydantic import HttpUrl
from strawberry.fastapi import GraphQLRouter

from app.domains.restaurants.presentation.graphql.context import get_graphql_context
from app.domains.restaurants.presentation.graphql.queries import RestaurantQuery


# Define custom scalars for Pydantic types
HttpUrlScalar = strawberry.scalar(
    NewType("HttpUrl", str),
    serialize=lambda v: str(v) if v else None,
    parse_value=lambda v: HttpUrl(v) if v else None,
    description="HTTP URL string",
)

DecimalScalar = strawberry.scalar(
    NewType("Decimal", float),
    serialize=lambda v: float(v),
    parse_value=lambda v: Decimal(str(v)),
    description="Decimal number represented as float",
)


@strawberry.type
class Query(RestaurantQuery):
    """Root GraphQL Query type.

    Combines all query resolvers from different subdomains.
    Currently includes:
    - Restaurant queries (restaurant, restaurants)

    Note:
        Use cases are injected into the context via FastAPI DI.
        Resolvers access them through info.context.
    """

    pass


# Create the GraphQL schema with scalar overrides for Pydantic types
schema = strawberry.Schema(
    query=Query,
    scalar_overrides={
        HttpUrl: HttpUrlScalar,
        Decimal: DecimalScalar,
    },
)


def create_graphql_router() -> GraphQLRouter:
    """Create and configure the GraphQL router for FastAPI.

    Uses FastAPI's dependency injection to populate the context,
    which is then accessed by resolvers via info.context.

    Returns:
        GraphQLRouter: Configured GraphQL router with GraphiQL enabled
    """
    return GraphQLRouter(
        schema,
        graphql_ide="graphiql",  # Enable GraphiQL interface for development
        path="/graphql",
        context_getter=get_graphql_context,  # Inject use cases via FastAPI DI
    )
