"""UTC datetime generation factory.

This module provides a centralized factory for generating UTC timestamps
used across all domain entities in the application.

Why UTC?
--------

UTC (Coordinated Universal Time) is used exclusively for all timestamps in
this application for several critical reasons:

1. **Timezone Independence**: UTC is a universal time standard without DST
   (Daylight Saving Time) transitions. This eliminates bugs related to:
   - DST transitions (spring forward, fall back)
   - Ambiguous times during DST changes
   - Timezone conversions gone wrong

2. **Database Consistency**: Storing all timestamps in UTC ensures consistent
   sorting and comparison across records, regardless of where they were created.
   Mixed timezones in a database lead to incorrect ordering and comparison bugs.

3. **Global Applications**: For applications serving multiple timezones, UTC
   provides a single source of truth. Display formatting in local time is done
   at the presentation layer, never in storage.

4. **API Interoperability**: Most APIs and microservices use UTC (ISO 8601).
   Using UTC natively eliminates conversion errors when integrating systems.

5. **Audit Trail Accuracy**: For legal and compliance reasons, audit timestamps
   must be unambiguous and universally comparable. UTC ensures this.

6. **No Leap Seconds Confusion**: Python's datetime.UTC handles leap seconds
   correctly according to the system's UTC implementation, avoiding time drift.

Best Practices:
    - **ALWAYS** store timestamps in UTC
    - **NEVER** store local time in the database
    - Convert to user's local timezone ONLY in the presentation layer
    - Use ISO 8601 format for API responses (YYYY-MM-DDTHH:MM:SSZ)

Common Mistakes to Avoid:
    ❌ datetime.now()              # Local time - NEVER use
    ❌ datetime.utcnow()           # Naive UTC - deprecated in Python 3.12
    ❌ datetime.now(timezone.utc)  # Works but verbose
    ✅ datetime.now(UTC)           # Correct - timezone-aware UTC

Example Problem:
    If you store timestamps in local time:
    - Record created at 2:30 AM on DST spring forward day
    - That time doesn't exist (clocks jump 2:00 → 3:00)
    - Database queries become ambiguous
    - Sorting breaks during DST transitions

References:
    - ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
    - Python datetime best practices: https://docs.python.org/3/library/datetime.html
    - UTC vs local time: https://stackoverflow.com/questions/2331592/why-use-utc-everywhere
"""

from datetime import UTC, datetime


def generate_utc_now() -> datetime:
    """Generate current UTC datetime.

    Returns the current moment in UTC timezone. The returned datetime object
    is timezone-aware (includes UTC timezone info), which prevents naive
    datetime comparison errors.

    Returns:
        Current datetime in UTC timezone (timezone-aware)

    Example:
        >>> now = generate_utc_now()
        >>> print(now)
        datetime.datetime(2024, 10, 24, 15, 30, 45, 123456, tzinfo=datetime.timezone.utc)
        >>> print(now.isoformat())
        "2024-10-24T15:30:45.123456+00:00"
        >>> now.tzinfo
        datetime.timezone.utc
    """
    return datetime.now(UTC)
