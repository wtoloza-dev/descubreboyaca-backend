"""Restaurant owner PostgreSQL implementation.

This module provides the PostgreSQL repository implementation for RestaurantOwner persistence operations.
PostgreSQL implementation inherits from the common SQL repository.
"""

from .common import SQLRestaurantOwnerRepository


class PostgreSQLRestaurantOwnerRepository(SQLRestaurantOwnerRepository):
    """Restaurant owner PostgreSQL implementation using async operations.

    This repository inherits all CRUD operations from SQLRestaurantOwnerRepository.
    Override methods here only when PostgreSQL-specific functionality is needed:
    - PostgreSQL-specific JSON operators
    - Full-text search
    - PostgreSQL-specific optimizations
    - Custom PostgreSQL query features

    For standard CRUD operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: SQLModel async session for database operations (inherited).
    """

    # PostgreSQL-specific methods or overrides can be added here if needed
    # Most of the time, this class will be empty (just inheriting)
    pass
