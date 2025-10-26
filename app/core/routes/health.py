"""Health check routes.

This module contains endpoints for monitoring application health and status.
"""

from datetime import datetime

from fastapi import APIRouter, status
from pydantic import BaseModel


router = APIRouter()


class HealthStatusResponse(BaseModel):
    """Health status model."""

    status: str = "healthy"
    timestamp: str = datetime.now().isoformat()


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
        dict[str, str]: Health status indicating the service is operational
    """
    return HealthStatusResponse()
