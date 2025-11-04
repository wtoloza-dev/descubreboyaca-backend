"""Owner dish routes.

This module aggregates all owner-accessible dish endpoints.
"""

from fastapi import APIRouter

from app.domains.restaurants.routes.dish.owner import create, delete, update


# Create router with owner prefix
router = APIRouter(prefix="/owner")

# Include routes
router.include_router(create.router)
router.include_router(update.router)
router.include_router(delete.router)
