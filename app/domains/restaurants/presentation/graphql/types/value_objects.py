"""GraphQL types for domain Value Objects.

This module defines GraphQL types for shared value objects from the domain layer,
such as GeoLocation and SocialMedia. Uses Strawberry's Pydantic integration
with all_fields=True for automatic field generation.

Architecture Note:
    This file bridges domain value objects with GraphQL types.

    Value Objects (Domain) → GraphQL Types (Presentation)
    - GeoLocation → GeoLocationType
    - SocialMedia → SocialMediaType

Why This File is Necessary:
    Strawberry requires ALL Pydantic types used in the schema to be explicitly
    registered with @strawberry.experimental.pydantic.type decorator.

    Even though RestaurantType uses all_fields=True, Strawberry cannot
    automatically infer nested Pydantic types like GeoLocation and SocialMedia.

    Without these registrations, you'll get:
    "UnregisteredTypeException: Cannot find a Strawberry Type for <class ...>"
"""

import strawberry

from app.shared.domain.value_objects import GeoLocation, SocialMedia


@strawberry.experimental.pydantic.type(
    model=GeoLocation,
    all_fields=True,
    description="Geographic location with latitude and longitude coordinates",
)
class GeoLocationType:
    """GraphQL type for geographic location.

    Automatically generated from the GeoLocation Pydantic model.
    All fields auto-generated for perfect synchronization.
    """

    pass


@strawberry.experimental.pydantic.type(
    model=SocialMedia,
    all_fields=True,
    description="Social media profile links",
)
class SocialMediaType:
    """GraphQL type for social media links.

    Automatically generated from the SocialMedia Pydantic model.
    All fields auto-generated for perfect synchronization.
    """

    pass
