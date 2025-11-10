"""Current user schemas.

This module defines response schemas for the current user endpoint.
"""

from pydantic import BaseModel

from app.domains.auth.presentation.api.schemas.user import UserSchemaResponse


class MeUserSchemaResponse(BaseModel):
    """Current user response schema.

    This schema is used for the /auth/me endpoint.

    Attributes:
        user: User data
    """

    user: UserSchemaResponse
