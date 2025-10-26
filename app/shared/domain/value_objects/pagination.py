"""Pagination value objects for database queries.

Simple value object for pagination parameters.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationParams:
    """Pagination parameters for database queries.

    Simple immutable value object containing offset and limit.

    Attributes:
        offset: Number of records to skip
        limit: Maximum number of records to return

    Example:
        >>> params = PaginationParams(offset=0, limit=20)
        >>> params.offset  # 0
        >>> params.limit  # 20
    """

    offset: int
    limit: int
