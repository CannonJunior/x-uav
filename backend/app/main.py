"""
X-UAV FastAPI Application

Main application entry point for the UAV comparison platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.arangodb import arango_connection
from app.db.postgresql import init_db
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting X-UAV Backend...")

    # Initialize PostgreSQL
    print("📊 Initializing PostgreSQL...")
    init_db()

    # Connect to ArangoDB
    print("🕸️  Connecting to ArangoDB...")
    arango_connection.connect()

    print("✅ X-UAV Backend started successfully!")
    print(f"📍 API available at http://localhost:{settings.port}{settings.api_v1_prefix}")
    print(f"📚 Documentation at http://localhost:{settings.port}/docs")

    yield

    # Shutdown
    print("🛑 Shutting down X-UAV Backend...")
    arango_connection.disconnect()
    print("✅ Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    version="0.1.0",
    description="UAV Comparison Platform with Graph Database and MCP Integration",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "X-UAV API",
        "version": "0.1.0",
        "docs": "/docs",
        "api": settings.api_v1_prefix
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "port": settings.port
    }
