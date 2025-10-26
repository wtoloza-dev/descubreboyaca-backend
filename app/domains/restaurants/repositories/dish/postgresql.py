"""Dish PostgreSQL implementation.

This module provides an asynchronous implementation of the Dish
repository for data persistence using SQLModel with PostgreSQL.

Note: The implementation is identical to SQLite because SQLModel
abstracts the database differences. This separation allows for
database-specific optimizations if needed in the future.
"""

from app.domains.restaurants.repositories.dish.sqlite import DishRepositorySQLite


class DishRepositoryPostgreSQL(DishRepositorySQLite):
    """Dish PostgreSQL implementation using async operations.

    Currently inherits from SQLite implementation as SQLModel provides
    database-agnostic operations. Can be extended with PostgreSQL-specific
    optimizations if needed (e.g., full-text search, JSON operators, etc.).

    Attributes:
        session: SQLModel async session for database operations
    """

    pass

