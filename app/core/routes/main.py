"""Main routes."""

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.core.settings import settings


router = APIRouter()


class RootResponse(BaseModel):
    """Root response model.

    Returns a welcome message for the API.
    """

    message: str = "Welcome to Descubre Boyacá API"
    version: str = settings.APP_VERSION
    scope: str = settings.SCOPE


@router.get(
    path="/",
    summary="Root endpoint",
    description="Returns a welcome message for the API",
    status_code=status.HTTP_200_OK,
)
async def root() -> RootResponse:
    """Root endpoint.

    Returns a welcome message for the API.
    """
    return RootResponse()
