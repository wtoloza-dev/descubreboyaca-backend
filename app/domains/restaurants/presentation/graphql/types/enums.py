"""GraphQL enumerations for restaurant domain.

This module re-exports domain enums with @strawberry.enum decorators for GraphQL.
Domain enums are the single source of truth - no duplication.

Architecture Note:
    We decorate domain enums directly with @strawberry.enum to avoid
    duplication. Domain enum names are normalized (ASCII-only) for
    GraphQL compatibility while values preserve correct Spanish spelling.
"""

import strawberry

from app.domains.restaurants.domain.enums import (
    CuisineType,
    EstablishmentType,
    RestaurantFeature,
)


# Decorate domain enums for GraphQL
# Since we can't inherit from enums, we decorate and re-export them
CuisineTypeEnum = strawberry.enum(
    CuisineType,
    description="Types of cuisine offered by restaurants",
)

EstablishmentTypeEnum = strawberry.enum(
    EstablishmentType,
    description="Types of food establishments",
)

RestaurantFeatureEnum = strawberry.enum(
    RestaurantFeature,
    description="Features and amenities available at restaurants",
)
