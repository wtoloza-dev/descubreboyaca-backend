"""Workflow test fixtures and configuration.

This module provides fixtures for workflow tests that interact with the
application via HTTP client rather than TestClient.
"""

import os
from collections.abc import AsyncGenerator

import httpx
import pytest


@pytest.fixture(name="workflow_base_url")
def fixture_workflow_base_url() -> str:
    """Get the base URL for workflow tests.

    Defaults to localhost but can be overridden via environment variable
    for testing against real deployments.

    Returns:
        str: Base URL for the API (e.g., http://localhost:8000)

    Environment Variables:
        WORKFLOW_BASE_URL: Override default localhost URL

    Example:
        >>> # Default usage (localhost)
        >>> pytest -m workflow
        >>>
        >>> # Test against staging
        >>> WORKFLOW_BASE_URL=https://staging.api.example.com pytest -m workflow
    """
    return os.getenv("WORKFLOW_BASE_URL", "http://localhost:8000")


@pytest.fixture(name="workflow_http_client")
async def fixture_workflow_http_client(
    workflow_base_url: str,
) -> AsyncGenerator[httpx.AsyncClient]:
    """Create an async HTTP client for workflow tests.

    This client makes real HTTP requests to the specified base URL.
    Unlike TestClient, this goes through the full HTTP stack including
    middleware, CORS, etc.

    Args:
        workflow_base_url: Base URL for API requests

    Yields:
        httpx.AsyncClient: Configured HTTP client

    Example:
        >>> @pytest.mark.workflow
        >>> async def test_create_restaurant(workflow_http_client):
        ...     response = await workflow_http_client.post(
        ...         "/api/v1/restaurants", json={"name": "Test Restaurant"}
        ...     )
        ...     assert response.status_code == 201
    """
    async with httpx.AsyncClient(
        base_url=workflow_base_url,
        timeout=30.0,
        follow_redirects=True,
    ) as client:
        yield client


@pytest.fixture(name="workflow_admin_client")
async def fixture_workflow_admin_client(
    workflow_base_url: str,
) -> AsyncGenerator[httpx.AsyncClient]:
    """Create an authenticated admin HTTP client for workflow tests.

    This client authenticates via /auth/login endpoint to get a real JWT token
    and includes it in all requests as a Bearer token.

    Args:
        workflow_base_url: Base URL for API requests

    Yields:
        httpx.AsyncClient: Configured HTTP client with admin auth

    Environment Variables:
        WORKFLOW_USERNAME: Admin username (default: john.doe@example.com)
        WORKFLOW_PASSWORD: Admin password (default: MySecurePassword123!)

    Example:
        >>> @pytest.mark.workflow
        >>> async def test_delete_restaurant(workflow_admin_client):
        ...     response = await workflow_admin_client.delete(
        ...         "/api/v1/restaurants/admin/123"
        ...     )
        ...     assert response.status_code == 204
    """
    # Get credentials from environment or use defaults
    username = os.getenv("WORKFLOW_USERNAME", "john.doe@example.com")
    password = os.getenv("WORKFLOW_PASSWORD", "MySecurePassword123!")

    async with httpx.AsyncClient(
        base_url=workflow_base_url,
        timeout=30.0,
        follow_redirects=True,
    ) as client:
        # Authenticate to get bearer token
        login_response = await client.post(
            "/auth/login/",
            json={"email": username, "password": password},
        )

        if login_response.status_code != 200:
            error_msg = (
                f"Failed to authenticate workflow admin client:\n"
                f"  URL: {workflow_base_url}/auth/login/\n"
                f"  Status: {login_response.status_code}\n"
                f"  Body: {login_response.text}\n"
                f"  User: {username}\n\n"
                f"Make sure:\n"
                f"  1. Server is running (uvicorn app.main:app --reload)\n"
                f"  2. User exists with correct credentials\n"
                f"  3. WORKFLOW_USERNAME and WORKFLOW_PASSWORD are correct"
            )
            raise RuntimeError(error_msg)

        # Extract access token
        token_data = login_response.json()
        access_token = token_data["access_token"]

        # Set authorization header for all subsequent requests
        client.headers.update({"Authorization": f"Bearer {access_token}"})

        yield client
