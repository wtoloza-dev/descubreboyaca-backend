"""Review statistics value object.

This module defines an immutable value object for aggregated review statistics.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ReviewStats(BaseModel):
    """Review statistics value object.

    Immutable value object representing aggregated statistics for reviews
    of a specific entity.

    Attributes:
        total_reviews: Total number of reviews
        average_rating: Average rating (0.00 to 5.00)
        rating_distribution: Count of reviews per rating (1-5)
    """

    total_reviews: int = Field(ge=0, description="Total number of reviews")
    average_rating: Decimal = Field(
        ge=Decimal("0.00"),
        le=Decimal("5.00"),
        decimal_places=2,
        description="Average rating from 0.00 to 5.00",
    )
    rating_distribution: dict[int, int] = Field(
        description="Distribution of ratings {1: count, 2: count, ...}"
    )

    model_config = ConfigDict(frozen=True)

    @property
    def five_star_count(self) -> int:
        """Get the count of 5-star reviews.

        Returns:
            Number of 5-star reviews
        """
        return self.rating_distribution.get(5, 0)

    @property
    def four_star_count(self) -> int:
        """Get the count of 4-star reviews.

        Returns:
            Number of 4-star reviews
        """
        return self.rating_distribution.get(4, 0)

    @property
    def three_star_count(self) -> int:
        """Get the count of 3-star reviews.

        Returns:
            Number of 3-star reviews
        """
        return self.rating_distribution.get(3, 0)

    @property
    def two_star_count(self) -> int:
        """Get the count of 2-star reviews.

        Returns:
            Number of 2-star reviews
        """
        return self.rating_distribution.get(2, 0)

    @property
    def one_star_count(self) -> int:
        """Get the count of 1-star reviews.

        Returns:
            Number of 1-star reviews
        """
        return self.rating_distribution.get(1, 0)

    @property
    def percentage_five_star(self) -> Decimal:
        """Calculate the percentage of 5-star reviews.

        Returns:
            Percentage of 5-star reviews (0.00 to 100.00)
        """
        if self.total_reviews == 0:
            return Decimal("0.00")
        percentage = (Decimal(self.five_star_count) / Decimal(self.total_reviews)) * 100
        return percentage.quantize(Decimal("0.01"))
