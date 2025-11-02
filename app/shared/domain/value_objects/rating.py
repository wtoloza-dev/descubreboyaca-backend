"""Rating value object.

This module defines an immutable rating value object with validation.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Rating(BaseModel):
    """Rating value object.

    Immutable value object representing an individual user rating from 1 to 5.
    This represents a single user's rating, not an aggregated average.

    For aggregated/average ratings (which can be decimal), use
    ReviewStats.average_rating instead.

    Characteristics:
    - Individual user rating (discrete choice)
    - Always integer (1, 2, 3, 4, or 5)
    - Immutable value object
    - Domain validation logic only

    Note: Presentation (stars, emojis, visual rendering) is handled by
    the frontend. This value object focuses purely on domain logic.

    Attributes:
        value: Integer rating from 1 to 5 (inclusive)

    Raises:
        ValueError: If rating is not between 1 and 5
    """

    model_config = ConfigDict(frozen=True)

    value: int = Field(ge=1, le=5, description="Rating value from 1 to 5")

    @field_validator("value", mode="before")
    @classmethod
    def validate_rating(cls, v: Any) -> int:
        """Validate that rating is between 1 and 5.

        Args:
            v: The rating value to validate

        Returns:
            The validated integer rating

        Raises:
            ValueError: If rating is not between 1 and 5
        """
        if not isinstance(v, int):
            try:
                v = int(v)
            except (ValueError, TypeError) as e:
                msg = f"Rating must be an integer, got {type(v).__name__}"
                raise ValueError(msg) from e

        if not 1 <= v <= 5:
            msg = f"Rating must be between 1 and 5, got {v}"
            raise ValueError(msg)

        return v

    def __int__(self) -> int:
        """Convert rating to integer for calculations.

        Returns:
            The rating value as an integer
        """
        return self.value

    def __str__(self) -> str:
        """Return string representation for debugging/logging.

        Returns:
            String representation of the rating value
        """
        return str(self.value)
