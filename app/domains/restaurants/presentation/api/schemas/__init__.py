"""Restaurant API schemas (DTOs).

This package contains Data Transfer Objects for restaurant API endpoints.

Schemas are organized following the same structure as routes:
- dish/
  - admin/ - Admin-only dish operations
  - owner/ - Owner/manager dish operations
  - public/ - Public dish operations
  - common/ - Shared base schemas
- restaurant/
  - admin/ - Admin-only restaurant operations
  - owner/ - Owner/manager restaurant operations
  - public/ - Public restaurant operations
  - common/ - Shared base schemas

Import schemas from their specific locations:
    from app.domains.restaurants.presentation.api.schemas.dish.admin.create import CreateDishSchemaRequest
    from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_restaurant_by_id import FindRestaurantByIdSchemaResponse
"""

# This file intentionally left minimal - import from specific submodules
# See Routes.md and Schemas.md documentation for structure details

__all__ = [
    "dish",
    "restaurant",
]
