"""User review routes.

Routes for authenticated users to manage their own reviews.
"""

from fastapi import APIRouter

from .list_my_reviews import router as list_reviews_router


router = APIRouter()

router.include_router(list_reviews_router)

__all__ = ["router"]
