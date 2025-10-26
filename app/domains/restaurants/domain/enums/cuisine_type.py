"""Cuisine type enumeration.

This module defines the types of cuisine that restaurants can offer.
"""

from enum import StrEnum


class CuisineType(StrEnum):
    """Types of cuisine offered by restaurants.

    This enum represents common cuisine types in Boyacá and Colombia.
    Values are in Spanish to match the local language.

    Example:
        >>> restaurant_data = RestaurantData(
        ...     name="La Casona",
        ...     cuisine_types=[CuisineType.BOYACENSE, CuisineType.COLOMBIANA],
        ...     ...
        ... )
    """

    # Colombian regional cuisines
    BOYACENSE = "boyacense"
    COLOMBIANA = "colombiana"
    SANTANDEREANA = "santandereana"
    ANTIOQUEÑA = "antioqueña"
    COSTEÑA = "costeña"
    LLANERA = "llanera"

    # International cuisines
    INTERNACIONAL = "internacional"
    ITALIANA = "italiana"
    MEXICANA = "mexicana"
    CHINA = "china"
    JAPONESA = "japonesa"
    PERUANA = "peruana"
    ARGENTINA = "argentina"
    ESPAÑOLA = "española"
    FRANCESA = "francesa"
    AMERICANA = "americana"

    # Special categories
    FUSION = "fusión"
    VEGETARIANA = "vegetariana"
    VEGANA = "vegana"
    PARRILLA = "parrilla"
    MARISCOS = "mariscos"
    COMIDA_RAPIDA = "comida_rápida"
    CAFETERIA = "cafetería"
    PANADERIA = "panadería"
    POSTRES = "postres"
    BAR = "bar"
