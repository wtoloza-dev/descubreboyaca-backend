"""Database health check routes.

This module contains endpoints for monitoring database connectivity and health.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.status.presentation.api.schemas.health_db import (
    DatabaseHealthResponse,
)
from app.shared.dependencies.sql import get_async_session_dependency


router = APIRouter()


@router.get(
    path="/health_db/",
    summary="Database health check endpoint",
    description="Returns the current health status of the database connection",
    status_code=status.HTTP_200_OK,
)
async def health_db_check(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> DatabaseHealthResponse:
    """Database health check endpoint.

    Verifies database connectivity by executing a simple query.

    Args:
        session: Async database session (injected via dependency)

    Returns:
        DatabaseHealthResponse: Database health status

    Raises:
        HTTPException: If database connection fails
    """
    try:
        # Execute a simple query to verify database is responsive
        result = await session.exec(text("SELECT 1"))
        result.first()

        # Determine database type based on scope
        db_type = "SQLite" if settings.SCOPE == "local" else "PostgreSQL"

        return DatabaseHealthResponse(
            status="healthy",
            database=db_type,
            message="Database connection is operational",
        )
    except Exception as e:
        return DatabaseHealthResponse(
            status="unhealthy",
            database="unknown",
            message=f"Database connection failed: {str(e)}",
        )
