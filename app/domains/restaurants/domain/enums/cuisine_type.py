"""Cuisine type enumeration.

This module defines the types of cuisine that restaurants can offer.

Note:
    Enum names are normalized (ASCII-only) for GraphQL compatibility.
    Values maintain the correct Spanish spelling with special characters.
"""

from enum import StrEnum


class CuisineType(StrEnum):
    """Types of cuisine offered by restaurants.

    This enum represents common cuisine types in Boyacá and Colombia.

    Names are normalized (e.g., ANTIOQUENA) for code/GraphQL compatibility,
    while values preserve correct Spanish spelling (e.g., "antioqueña").

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
    ANTIOQUENA = "antioqueña"  # Name normalized, value preserves ñ
    COSTENA = "costeña"  # Name normalized, value preserves ñ
    LLANERA = "llanera"

    # International cuisines
    INTERNACIONAL = "internacional"
    ITALIANA = "italiana"
    MEXICANA = "mexicana"
    CHINA = "china"
    JAPONESA = "japonesa"
    PERUANA = "peruana"
    ARGENTINA = "argentina"
    ESPANOLA = "española"  # Name normalized, value preserves ñ
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
