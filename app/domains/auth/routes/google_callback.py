"""Google OAuth callback route.

This module handles the OAuth callback from Google after user authentication.
"""

from fastapi import APIRouter, Depends, Query, status

from app.domains.auth.dependencies.security import get_google_oauth_client_dependency
from app.domains.auth.dependencies.sql import get_auth_service_dependency
from app.domains.auth.schemas import (
    GoogleCallbackUserSchemaResponse,
    UserSchemaResponse,
)
from app.domains.auth.services import AuthService, GoogleOAuthClient


router = APIRouter()


@router.get(
    path="/google/callback",
    status_code=status.HTTP_200_OK,
    summary="Google OAuth callback",
    description="Handle OAuth callback from Google and authenticate user",
)
async def handle_google_callback(
    code: str = Query(..., description="Authorization code from Google"),
    auth_service: AuthService = Depends(get_auth_service_dependency),
    google_oauth_client: GoogleOAuthClient = Depends(
        get_google_oauth_client_dependency
    ),
) -> GoogleCallbackUserSchemaResponse:
    """Handle Google OAuth callback.

    This endpoint receives the authorization code from Google,
    exchanges it for user profile data, and creates/authenticates the user.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        code: Authorization code from Google OAuth callback
        auth_service: Auth service dependency
        google_oauth_service: Google OAuth service dependency

    Returns:
        GoogleCallbackUserSchemaResponse with JWT tokens and user data

    Raises:
        AuthenticationException: If Google authentication fails
        UserInactiveException: If user account is inactive
    """
    # Get user profile from Google
    oauth_profile = await google_oauth_client.get_user_profile(code)

    # Authenticate or register user
    tokens, user = await auth_service.login_with_oauth(oauth_profile)

    return GoogleCallbackUserSchemaResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token or "",
        token_type=tokens.token_type,
        user=UserSchemaResponse.model_validate(user),
    )
