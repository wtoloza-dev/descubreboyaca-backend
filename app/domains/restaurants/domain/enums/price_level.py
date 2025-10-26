"""Price level enumeration.

This module defines price range categories for restaurants.
"""

from enum import IntEnum


class PriceLevel(IntEnum):
    """Price range categories for restaurants.

    Represents the average cost per person for a meal.
    Based on Colombian peso (COP) ranges.

    Attributes:
        BUDGET: Economic - Less than $20,000 COP per person
        MODERATE: Moderate - $20,000 - $40,000 COP per person
        EXPENSIVE: Expensive - $40,000 - $80,000 COP per person
        LUXURY: Luxury - More than $80,000 COP per person

    Example:
        >>> restaurant_data = RestaurantData(
        ...     name="La Casona",
        ...     price_level=PriceLevel.MODERATE,
        ...     ...
        ... )
    """

    BUDGET = 1
    MODERATE = 2
    EXPENSIVE = 3
    LUXURY = 4

    @property
    def display_name(self) -> str:
        """Get display name in Spanish.

        Returns:
            str: Human-readable name in Spanish
        """
        names = {
            1: "Económico",
            2: "Moderado",
            3: "Caro",
            4: "Lujo",
        }
        return names[self.value]

    @property
    def price_range(self) -> str:
        """Get price range in Colombian pesos.

        Returns:
            str: Price range description
        """
        ranges = {
            1: "< $20,000 COP",
            2: "$20,000 - $40,000 COP",
            3: "$40,000 - $80,000 COP",
            4: "> $80,000 COP",
        }
        return ranges[self.value]

    @property
    def symbol(self) -> str:
        """Get price level symbol.

        Returns:
            str: Symbol representation ($ to $$$$)
        """
        return "$" * self.value
