"""Default constants.

This module defines default values used across the application.
"""

# Geographic defaults for Colombia and Boyacá
DEFAULT_COUNTRY = "Colombia"
DEFAULT_STATE = "Boyacá"
DEFAULT_CURRENCY = "COP"

# Boyacá main cities coordinates (for reference)
TUNJA_COORDINATES = {"latitude": 5.5353, "longitude": -73.3678}
DUITAMA_COORDINATES = {"latitude": 5.8244, "longitude": -73.0336}
SOGAMOSO_COORDINATES = {"latitude": 5.7167, "longitude": -72.9333}
PAIPA_COORDINATES = {"latitude": 5.7794, "longitude": -73.1153}
VILLA_DE_LEYVA_COORDINATES = {"latitude": 5.6361, "longitude": -73.5264}

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# String length limits
MAX_NAME_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 1000
MAX_ADDRESS_LENGTH = 500
MAX_NOTE_LENGTH = 1000
