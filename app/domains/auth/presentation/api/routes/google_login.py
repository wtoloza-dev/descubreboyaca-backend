"""Google OAuth login initiation route.

This module handles the initiation of Google OAuth authentication flow.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.auth.application.services import GoogleOAuthClient
from app.domains.auth.infrastructure.dependencies.security import (
    get_google_oauth_client_dependency,
)
from app.domains.auth.presentation.api.schemas import GoogleLoginUserSchemaResponse


router = APIRouter()


@router.get(
    path="/google/login/",
    status_code=status.HTTP_200_OK,
    summary="Initiate Google OAuth login",
    description="Get the Google OAuth authorization URL to redirect the user to",
)
async def handle_google_login(
    google_oauth_client: Annotated[
        GoogleOAuthClient, Depends(get_google_oauth_client_dependency)
    ],
) -> GoogleLoginUserSchemaResponse:
    """Initiate Google OAuth login flow.

    This endpoint returns the Google authorization URL where the user
    should be redirected to authenticate with Google.

    Args:
        google_oauth_client: Google OAuth client dependency

    Returns:
        GoogleLoginUserSchemaResponse with authorization URL
    """
    authorization_url = google_oauth_client.get_authorization_url()

    return GoogleLoginUserSchemaResponse(
        authorization_url=authorization_url,
        message="Redirect user to this URL for Google authentication",
    )
