"""Geolocation value object.

This module defines the GeoLocation value object for representing geographic coordinates.
"""

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class GeoLocation(BaseModel):
    """Geographic location value object.

    Represents a point on Earth using latitude and longitude coordinates.
    This is an immutable value object that can be shared across domains.

    Attributes:
        latitude: Latitude coordinate (-90 to 90)
        longitude: Longitude coordinate (-180 to 180)

    Example:
        >>> location = GeoLocation(
        ...     latitude=Decimal("5.5353"), longitude=Decimal("-73.3678")
        ... )
        >>> # Tunja, Boyacá coordinates
    """

    model_config = ConfigDict(frozen=True)

    latitude: Decimal = Field(
        ...,
        description="Latitude in decimal degrees",
        ge=-90,
        le=90,
        decimal_places=6,
    )
    longitude: Decimal = Field(
        ...,
        description="Longitude in decimal degrees",
        ge=-180,
        le=180,
        decimal_places=6,
    )

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def validate_decimal(cls, v: Any) -> Decimal:
        """Validate and convert to Decimal with proper precision.

        Args:
            v: Value to validate

        Returns:
            Decimal representation of the value with 8 decimal places

        Raises:
            ValueError: If value cannot be converted to Decimal
        """
        if isinstance(v, Decimal):
            # Quantize to 8 decimal places for coordinate precision (~1mm)
            return v.quantize(Decimal("0.00000001"))
        if isinstance(v, (int, float, str)):
            decimal_value = Decimal(str(v))
            return decimal_value.quantize(Decimal("0.00000001"))
        msg = f"Cannot convert {type(v)} to Decimal"
        raise ValueError(msg)

    @field_serializer("latitude", "longitude")
    def serialize_decimal(self, value: Decimal) -> float:
        """Serialize Decimal to float for JSON output.

        This ensures coordinates are serialized as clean floats with
        reasonable precision (8 decimals = ~1mm accuracy).

        Args:
            value: Decimal value to serialize

        Returns:
            Float with up to 8 decimal places
        """
        return round(float(value), 8)

    def to_dict(self) -> dict[str, float]:
        """Convert to dictionary with float values.

        Returns:
            Dictionary with latitude and longitude as floats with 8 decimal precision
        """
        return {
            "latitude": round(float(self.latitude), 8),
            "longitude": round(float(self.longitude), 8),
        }
