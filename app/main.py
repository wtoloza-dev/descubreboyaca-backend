"""Main FastAPI application entry point.

This module initializes and configures the FastAPI application with all
required middleware, routers, and settings using the Application Factory pattern.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.errors import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.middlewares import ObservabilityMiddleware
from app.core.settings import settings
from app.domains.audit.presentation.api.routes import router as audit_router
from app.domains.auth.presentation.api.routes import router as auth_router
from app.domains.favorites.presentation.api.routes import router as favorites_router
from app.domains.restaurants.presentation.api.routes import router as restaurants_router
from app.domains.reviews.presentation.api.routes import router as reviews_router
from app.domains.status.presentation.api.routes import router as status_router
from app.domains.users.presentation.api.routes import router as users_router


def register_routers(app: FastAPI) -> None:
    """Register all application routers.

    This function registers all application routers with the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Status and auth routers
    app.include_router(status_router, include_in_schema=settings.DEBUG)
    app.include_router(auth_router)

    # API v1 routers
    api_v1_router = APIRouter(prefix="/api/v1")
    api_v1_router.include_router(restaurants_router)
    api_v1_router.include_router(favorites_router)
    api_v1_router.include_router(reviews_router)
    api_v1_router.include_router(users_router)
    api_v1_router.include_router(audit_router)
    app.include_router(api_v1_router)


def register_middlewares(app: FastAPI) -> None:
    """Register application middlewares.

    This function registers all middlewares with the FastAPI application,
    including CORS and observability middleware.

    Args:
        app: FastAPI application instance
    """
    # Register observability middleware
    app.add_middleware(ObservabilityMiddleware)

    # Register CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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
        redirect_slashes=True,  # Redirige /endpoint/ a /endpoint y viceversa
        lifespan=lifespan,  # Manage database lifecycle
    )

    # Register middlewares
    register_middlewares(app)

    # Register exception handlers
    register_exception_handlers(app)

    # Register all routers
    register_routers(app)

    return app


# Create application instance for FastAPI CLI and uvicorn
app = create_app()
