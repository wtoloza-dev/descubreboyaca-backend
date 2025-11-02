"""Perception enumeration.

This module defines a qualitative 4-level perception system for rating
experiences without the bias of numeric scales.
"""

from enum import StrEnum


class Perception(StrEnum):
    """Perception enumeration.

    A 4-level qualitative rating system that eliminates the bias of
    numeric scales. Unlike 5-star ratings which tend to inflate toward
    4-5 stars and create a "safe middle" choice, this system forces a
    clear decision.

    Psychological advantages:
    - No "safe middle" option (forces honest assessment)
    - More conversational and natural
    - Reduces rating inflation
    - Cognitively simpler (less decision fatigue)
    - More even distribution of ratings

    Use cases:
    - Quick feedback without overthinking
    - Personal journal entries (intimate, honest)
    - Filtering experiences by quality
    - Sentiment analysis

    Complementary to numeric ratings:
    - Perception: Qualitative, personal, quick
    - Rating (1-5): Quantitative, precise, mathematical

    Note: Visual presentation (emojis, icons, colors) is handled by
    the frontend. This enum focuses purely on domain logic.

    Attributes:
        BAD: Disappointing or poor experience
        REGULAR: Acceptable but unremarkable experience
        GOOD: Satisfying and recommended experience
        AMAZING: Outstanding and memorable experience
    """

    BAD = "bad"
    REGULAR = "regular"
    GOOD = "good"
    AMAZING = "amazing"

    def to_order(self) -> int:
        """Convert perception to ordinal value for sorting/comparison.

        Returns:
            Integer from 1 (BAD) to 4 (AMAZING) for ordering
        """
        mapping = {
            Perception.BAD: 1,
            Perception.REGULAR: 2,
            Perception.GOOD: 3,
            Perception.AMAZING: 4,
        }
        return mapping[self]

    def to_rating_range(self) -> tuple[int, int]:
        """Suggest approximate equivalent rating range.

        This is a suggested mapping to 1-5 star ratings for reference only.
        Both systems are complementary and independent - this is not meant
        to be used as a strict conversion.

        Returns:
            Tuple of (min_rating, max_rating) in 1-5 scale
        """
        mapping = {
            Perception.BAD: (1, 2),
            Perception.REGULAR: (2, 3),
            Perception.GOOD: (3, 4),
            Perception.AMAZING: (4, 5),
        }
        return mapping[self]

    @classmethod
    def from_rating(cls, rating: int) -> Perception:
        """Suggest perception from numeric rating (approximate conversion).

        This is an approximate conversion from 1-5 star ratings to
        perception levels. Not meant to be used as strict mapping,
        just a reasonable default.

        Args:
            rating: Numeric rating from 1 to 5

        Returns:
            Suggested perception level

        Raises:
            ValueError: If rating is not between 1 and 5
        """
        if not 1 <= rating <= 5:
            msg = f"Rating must be between 1 and 5, got {rating}"
            raise ValueError(msg)

        if rating <= 2:
            return cls.BAD
        if rating == 3:
            return cls.REGULAR
        if rating == 4:
            return cls.GOOD
        return cls.AMAZING

    def __lt__(self, other: object) -> bool:
        """Compare perceptions for ordering (BAD < REGULAR < GOOD < AMAZING).

        Args:
            other: Another Perception instance

        Returns:
            True if self is less than other

        Raises:
            TypeError: If other is not a Perception instance
        """
        if not isinstance(other, Perception):
            return NotImplemented
        return self.to_order() < other.to_order()

    def __le__(self, other: object) -> bool:
        """Compare perceptions for ordering.

        Args:
            other: Another Perception instance

        Returns:
            True if self is less than or equal to other

        Raises:
            TypeError: If other is not a Perception instance
        """
        if not isinstance(other, Perception):
            return NotImplemented
        return self.to_order() <= other.to_order()

    def __gt__(self, other: object) -> bool:
        """Compare perceptions for ordering.

        Args:
            other: Another Perception instance

        Returns:
            True if self is greater than other

        Raises:
            TypeError: If other is not a Perception instance
        """
        if not isinstance(other, Perception):
            return NotImplemented
        return self.to_order() > other.to_order()

    def __ge__(self, other: object) -> bool:
        """Compare perceptions for ordering.

        Args:
            other: Another Perception instance

        Returns:
            True if self is greater than or equal to other

        Raises:
            TypeError: If other is not a Perception instance
        """
        if not isinstance(other, Perception):
            return NotImplemented
        return self.to_order() >= other.to_order()
