"""Health check schemas."""

from datetime import datetime

from pydantic import BaseModel


class HealthStatusResponse(BaseModel):
    """Health status model."""

    status: str = "healthy"
    timestamp: str = datetime.now().isoformat()
