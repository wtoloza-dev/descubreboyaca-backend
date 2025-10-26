"""Establishment type enumeration.

This module defines the types of food establishments.
"""

from enum import StrEnum


class EstablishmentType(StrEnum):
    """Types of food establishments.

    Represents different categories of food service businesses.
    Values are in English snake_case for consistency with code conventions,
    but have display names in Spanish.

    Example:
        >>> restaurant_data = RestaurantData(
        ...     name="Aroma Café Restaurante",
        ...     establishment_types=[
        ...         EstablishmentType.CAFE,
        ...         EstablishmentType.RESTAURANT,
        ...     ],
        ...     ...
        ... )
    """

    RESTAURANT = "restaurant"
    CAFE = "cafe"
    BAKERY = "bakery"
    BAR = "bar"
    PUB = "pub"
    FOOD_TRUCK = "food_truck"
    FAST_FOOD = "fast_food"
    FINE_DINING = "fine_dining"
    BUFFET = "buffet"
    CAFETERIA = "cafeteria"
    BISTRO = "bistro"
    PIZZERIA = "pizzeria"
    ICE_CREAM_SHOP = "ice_cream_shop"
    JUICE_BAR = "juice_bar"

    @property
    def display_name(self) -> str:
        """Get display name in Spanish.

        Returns:
            str: Human-readable name in Spanish
        """
        names = {
            "restaurant": "Restaurante",
            "cafe": "Cafetería",
            "bakery": "Panadería",
            "bar": "Bar",
            "pub": "Pub",
            "food_truck": "Food Truck",
            "fast_food": "Comida Rápida",
            "fine_dining": "Alta Cocina",
            "buffet": "Buffet",
            "cafeteria": "Cafetería",
            "bistro": "Bistró",
            "pizzeria": "Pizzería",
            "ice_cream_shop": "Heladería",
            "juice_bar": "Jugos Naturales",
        }
        return names.get(self, self.replace("_", " ").title())
