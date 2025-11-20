"""Root endpoint schemas."""

from pydantic import BaseModel

from app.core.settings import settings


class RootResponse(BaseModel):
    """Root response model.

    Returns a welcome message for the API.
    """

    message: str = "Welcome to Descubre Boyacá API"
    version: str = settings.APP_VERSION
    scope: str = settings.SCOPE
