"""GraphQL types for restaurant domain.

This module exports all GraphQL types for the restaurant domain.

CRITICAL: Import order matters for Strawberry's type registration!
    DO NOT let auto-formatters reorder these imports!
"""

# ruff: noqa: I001, E402
# fmt: off
# isort: skip_file

# ============================================================================
# IMPORT ORDER IS CRITICAL! Do not reorder!
# 
# Dependency hierarchy (from most basic to most complex):
#   1. Enums          - No dependencies
#   2. Value Objects  - May depend on enums
#   3. Entities       - Depend on enums + value objects
#
# Strawberry registers types when modules are imported via decorators.
# All base types MUST be registered BEFORE entities that use them.
# ============================================================================

# Step 1: Register enums FIRST (most basic, no dependencies)
from app.domains.restaurants.presentation.graphql.types.enums import (
    CuisineTypeEnum,
    EstablishmentTypeEnum,
    RestaurantFeatureEnum,
)

# Step 2: Register value objects (may depend on enums)
from app.domains.restaurants.presentation.graphql.types.value_objects import (
    GeoLocationType,
    SocialMediaType,
)

# Step 3: Register entity types (depend on enums + value objects)
from app.domains.restaurants.presentation.graphql.types.restaurant import (
    RestaurantConnection,
    RestaurantType,
)


__all__ = [
    "GeoLocationType",
    "SocialMediaType",
    "CuisineTypeEnum",
    "EstablishmentTypeEnum",
    "RestaurantFeatureEnum",
    "RestaurantType",
    "RestaurantConnection",
]
