"""Main FastAPI application entry point.

This module initializes and configures the FastAPI application with all
required middleware, routers, and settings using the Application Factory pattern.
"""

from fastapi import FastAPI

from app.core.routes import router as core_router
from app.core.settings import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    This function implements the Application Factory pattern, allowing for
    better testability and flexibility in configuration.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME + " " + settings.SCOPE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION + " " + settings.SCOPE,
    )

    # Register core routes
    app.include_router(core_router)

    # TODO: Add middleware
    # from fastapi.middleware.cors import CORSMiddleware
    # app.add_middleware(CORSMiddleware, ...)

    # TODO: Add event handlers
    # @app.on_event("startup")
    # async def startup_event():
    #     # Initialize database, cache, etc.
    #     pass
    #
    # @app.on_event("shutdown")
    # async def shutdown_event():
    #     # Cleanup resources
    #     pass

    return app


# Create application instance for FastAPI CLI and uvicorn
app = create_app()
