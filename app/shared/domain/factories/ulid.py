"""ULID generation factory.

This module provides a centralized factory for generating ULID identifiers
used across all domain entities in the application.

Why ULID?
---------

ULID (Universally Unique Lexicographically Sortable Identifier) is chosen over
traditional UUIDs (v4) for several key advantages:

1. **Lexicographic Sorting**: ULIDs are naturally sortable by creation time,
   which means database indexes perform better and queries are more efficient.
   Unlike UUID v4, which is random, ULIDs maintain chronological order.

2. **Better Database Performance**: Because ULIDs are sortable, they create
   better B-tree indexes in databases. Random UUIDs cause index fragmentation
   and degraded performance over time, especially in high-write scenarios.

3. **128-bit Compatibility**: Like UUIDs, ULIDs are 128 bits, but encoded
   in 26 characters using Crockford's Base32 (vs 36 for UUID with hyphens).
   This makes them more compact in storage and URLs.

4. **Time Component**: The first 48 bits encode a timestamp (milliseconds since
   Unix epoch), which allows you to extract creation time from the ID itself.
   This is useful for debugging and audit trails.

5. **No Collisions**: The remaining 80 bits are random, providing excellent
   uniqueness guarantees (same as UUID v4's randomness).

6. **Case Insensitive**: Uses Crockford's Base32, which avoids ambiguous
   characters (0, O, I, L) and is case-insensitive, reducing user errors.

Example ULID:
    01ARZ3NDEKTSV4RRFFQ69G5FAV
    └─┬─┘└─────────┬───────────┘
      │           │
      │           └─ 80-bit random
      └─ 48-bit timestamp

Performance Impact:
    In production databases with millions of records, ULID-based indexes
    maintain consistent O(log n) performance, while random UUID indexes
    degrade significantly due to fragmentation and page splits.

References:
    - ULID Specification: https://github.com/ulid/spec
    - Database Index Performance: https://www.2ndquadrant.com/en/blog/sequential-uuid-generators/
"""

from ulid import ULID


def generate_ulid() -> str:
    """Generate a ULID string identifier.

    Creates a new ULID with the current timestamp and cryptographically
    secure random component. The result is a 26-character string that is
    both unique and sortable.

    Returns:
        A 26-character ULID string (Crockford's Base32 encoded)

    Example:
        >>> ulid_id = generate_ulid()
        >>> print(ulid_id)
        "01HQZX8YV2KNP3R5J6M7F8G9H0"
        >>> len(ulid_id)
        26
    """
    return str(ULID())
