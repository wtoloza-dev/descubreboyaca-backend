"""Public review routes.

Routes for public access to reviews (no authentication required).
"""

from fastapi import APIRouter

from .list_dish_reviews import router as list_dish_reviews_router
from .list_restaurant_reviews import router as list_restaurant_reviews_router


router = APIRouter()

router.include_router(list_restaurant_reviews_router)
router.include_router(list_dish_reviews_router)

__all__ = ["router"]
