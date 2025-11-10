"""Dietary restriction enumeration.

This module defines dietary restrictions and special dietary considerations
that can be associated with dishes.
"""

from enum import StrEnum


class DietaryRestriction(StrEnum):
    """Dietary restrictions and special diet indicators.

    These tags help customers with specific dietary needs identify
    suitable dishes quickly.
    """

    # Main dietary restrictions
    VEGETARIAN = "vegetarian"  # Vegetariano
    VEGAN = "vegan"  # Vegano

    # Allergens and intolerances
    GLUTEN_FREE = "gluten_free"  # Sin gluten
    LACTOSE_FREE = "lactose_free"  # Sin lactosa
    NUT_FREE = "nut_free"  # Sin frutos secos

    # Religious/cultural dietary laws
    HALAL = "halal"  # Halal
    KOSHER = "kosher"  # Kosher

    # Health-conscious options
    LOW_CALORIE = "low_calorie"  # Bajo en calorías
    LOW_SODIUM = "low_sodium"  # Bajo en sodio
    LOW_CARB = "low_carb"  # Bajo en carbohidratos
    LOW_FAT = "low_fat"  # Bajo en grasas
    HIGH_PROTEIN = "high_protein"  # Alto en proteína

    # Spice level
    SPICY = "spicy"  # Picante
    MILD = "mild"  # Suave

    # Other
    ORGANIC = "organic"  # Orgánico
    RAW = "raw"  # Crudo
    CONTAINS_ALCOHOL = "contains_alcohol"  # Contiene alcohol
