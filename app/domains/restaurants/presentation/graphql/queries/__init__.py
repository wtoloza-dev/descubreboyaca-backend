"""GraphQL queries for restaurant domain.

This module exports all GraphQL query resolvers for the restaurant domain.
"""

from app.domains.restaurants.presentation.graphql.queries.restaurant import (
    RestaurantQuery,
)


__all__ = [
    "RestaurantQuery",
]
