"""Root endpoint routes."""

from fastapi import APIRouter, status

from app.domains.status.presentation.api.schemas.root import RootResponse


router = APIRouter()


@router.get(
    path="/",
    summary="Root endpoint",
    description="Returns a welcome message for the API",
    status_code=status.HTTP_200_OK,
)
async def root() -> RootResponse:
    """Root endpoint.

    Returns a welcome message for the API.

    Returns:
        RootResponse: Welcome message with API information
    """
    return RootResponse()
