"""Restaurant use cases.

This package contains all use cases related to restaurant operations.
Each use case represents a single business operation.
"""

from app.domains.restaurants.application.use_cases.restaurant.count_restaurants import (
    CountRestaurantsUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.create_restaurant import (
    CreateRestaurantUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.delete_restaurant import (
    DeleteRestaurantUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.find_restaurant_by_id import (
    FindRestaurantByIdUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.find_restaurants import (
    FindRestaurantsUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.list_restaurants_by_city import (
    ListRestaurantsByCityUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.list_user_favorite_restaurants import (
    ListUserFavoriteRestaurantsUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant.update_restaurant import (
    UpdateRestaurantUseCase,
)


__all__ = [
    "CountRestaurantsUseCase",
    "CreateRestaurantUseCase",
    "DeleteRestaurantUseCase",
    "FindRestaurantByIdUseCase",
    "FindRestaurantsUseCase",
    "ListRestaurantsByCityUseCase",
    "ListUserFavoriteRestaurantsUseCase",
    "UpdateRestaurantUseCase",
]
