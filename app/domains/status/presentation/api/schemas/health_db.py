"""Database health check schemas."""

from datetime import datetime

from pydantic import BaseModel


class DatabaseHealthResponse(BaseModel):
    """Database health status model."""

    status: str
    database: str
    timestamp: str = datetime.now().isoformat()
    message: str | None = None
