"""Restaurant feature enumeration.

This module defines features and amenities that restaurants can offer.
"""

from enum import StrEnum


class RestaurantFeature(StrEnum):
    """Features and amenities available at restaurants.

    Represents common services and facilities offered by restaurants.
    Values are in English snake_case for consistency with code conventions.

    Example:
        >>> restaurant_data = RestaurantData(
        ...     name="La Casona",
        ...     features=[
        ...         RestaurantFeature.WIFI,
        ...         RestaurantFeature.PARKING,
        ...         RestaurantFeature.OUTDOOR_SEATING,
        ...     ],
        ...     ...
        ... )
    """

    # Connectivity
    WIFI = "wifi"
    TV = "tv"

    # Seating and space
    PARKING = "parking"
    OUTDOOR_SEATING = "outdoor_seating"
    PRIVATE_ROOMS = "private_rooms"
    BAR_AREA = "bar_area"
    TERRACE = "terrace"

    # Accessibility
    WHEELCHAIR_ACCESSIBLE = "wheelchair_accessible"
    ELEVATOR = "elevator"

    # Services
    DELIVERY = "delivery"
    TAKEOUT = "takeout"
    RESERVATIONS = "reservations"
    ONLINE_ORDER = "online_order"
    WAITER_SERVICE = "waiter_service"
    SELF_SERVICE = "self_service"

    # Payment
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH_ONLY = "cash_only"
    MOBILE_PAYMENT = "mobile_payment"

    # Family and pets
    KIDS_MENU = "kids_menu"
    HIGH_CHAIRS = "high_chairs"
    KIDS_PLAY_AREA = "kids_play_area"
    PET_FRIENDLY = "pet_friendly"
    FAMILY_FRIENDLY = "family_friendly"

    # Dietary
    VEGETARIAN_OPTIONS = "vegetarian_options"
    VEGAN_OPTIONS = "vegan_options"
    GLUTEN_FREE_OPTIONS = "gluten_free_options"
    HALAL = "halal"
    KOSHER = "kosher"

    # Entertainment
    LIVE_MUSIC = "live_music"
    SPORTS_ON_TV = "sports_on_tv"
    KARAOKE = "karaoke"
    DANCE_FLOOR = "dance_floor"

    # Atmosphere
    ROMANTIC = "romantic"
    CASUAL = "casual"
    FINE_DINING = "fine_dining"
    BUSINESS_MEETINGS = "business_meetings"

    # Special services
    CATERING = "catering"
    PRIVATE_EVENTS = "private_events"
    BUFFET = "buffet"
    BREAKFAST = "breakfast"
    BRUNCH = "brunch"
    LUNCH = "lunch"
    DINNER = "dinner"
    LATE_NIGHT = "late_night"

    @property
    def display_name(self) -> str:
        """Get display name in Spanish.

        Returns:
            str: Human-readable name in Spanish
        """
        names = {
            # Connectivity
            "wifi": "WiFi",
            "tv": "TV",
            # Seating
            "parking": "Estacionamiento",
            "outdoor_seating": "Mesas al aire libre",
            "private_rooms": "Salones privados",
            "bar_area": "Área de bar",
            "terrace": "Terraza",
            # Accessibility
            "wheelchair_accessible": "Accesible para sillas de ruedas",
            "elevator": "Ascensor",
            # Services
            "delivery": "Domicilio",
            "takeout": "Para llevar",
            "reservations": "Reservas",
            "online_order": "Pedido en línea",
            "waiter_service": "Servicio a la mesa",
            "self_service": "Autoservicio",
            # Payment
            "credit_card": "Tarjeta de crédito",
            "debit_card": "Tarjeta débito",
            "cash_only": "Solo efectivo",
            "mobile_payment": "Pago móvil",
            # Family
            "kids_menu": "Menú infantil",
            "high_chairs": "Sillas altas",
            "kids_play_area": "Zona de juegos infantil",
            "pet_friendly": "Admite mascotas",
            "family_friendly": "Familiar",
            # Dietary
            "vegetarian_options": "Opciones vegetarianas",
            "vegan_options": "Opciones veganas",
            "gluten_free_options": "Opciones sin gluten",
            "halal": "Halal",
            "kosher": "Kosher",
            # Entertainment
            "live_music": "Música en vivo",
            "sports_on_tv": "Deportes en TV",
            "karaoke": "Karaoke",
            "dance_floor": "Pista de baile",
            # Atmosphere
            "romantic": "Romántico",
            "casual": "Casual",
            "fine_dining": "Alta cocina",
            "business_meetings": "Reuniones de negocios",
            # Special
            "catering": "Catering",
            "private_events": "Eventos privados",
            "buffet": "Buffet",
            "breakfast": "Desayuno",
            "brunch": "Brunch",
            "lunch": "Almuerzo",
            "dinner": "Cena",
            "late_night": "Trasnoche",
        }
        return names.get(self, self.replace("_", " ").title())
