"""Google OAuth login initiation schemas.

This module defines response schemas for Google OAuth login initiation.
"""

from pydantic import BaseModel


class GoogleLoginUserSchemaResponse(BaseModel):
    """Google OAuth login initiation response.

    Attributes:
        authorization_url: URL to redirect user for Google authentication
        message: Instruction message
    """

    authorization_url: str
    message: str = "Redirect user to this URL for Google authentication"
