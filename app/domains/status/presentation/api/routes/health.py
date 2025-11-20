"""Health check routes.

This module contains endpoints for monitoring application health and status.
"""

from fastapi import APIRouter, status

from app.domains.status.presentation.api.schemas.health import HealthStatusResponse


router = APIRouter()


@router.get(
    path="/health/",
    summary="Health check endpoint",
    description="Returns the current health status of the application",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> HealthStatusResponse:
    """Health check endpoint.

    Returns the current health status of the application.

    Returns:
        HealthStatusResponse: Health status indicating the service is operational
    """
    return HealthStatusResponse()
