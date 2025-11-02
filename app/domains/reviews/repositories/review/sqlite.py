"""Review repository SQLite implementation.

This module implements the review repository for SQLite database operations.
SQLite implementation inherits from PostgreSQL as they share the same SQL dialect
for the operations we're using.
"""

from .postgresql import ReviewRepositoryPostgreSQL


class ReviewRepositorySQLite(ReviewRepositoryPostgreSQL):
    """SQLite repository for review database operations.

    This repository inherits from ReviewRepositoryPostgreSQL as SQLite
    and PostgreSQL share compatible SQL syntax for our use cases.

    If SQLite-specific optimizations or different behavior are needed,
    methods can be overridden here.
    """

    pass
