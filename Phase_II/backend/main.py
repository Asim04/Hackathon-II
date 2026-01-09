"""
Main FastAPI application.

This module initializes the FastAPI app with CORS middleware,
database connection, and API routes.
"""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from db import create_db_and_tables, close_db_connection
from routes import auth, tasks

# Fix for Windows: psycopg requires SelectorEventLoop, not ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("ENVIRONMENT") == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Startup:
        - Create database tables if they don't exist

    Shutdown:
        - Close database connection pool
    """
    # Startup: Create database tables
    logger.info("Starting Todo API application...")
    try:
        await create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise

    yield

    # Shutdown: Close database connections
    logger.info("Shutting down Todo API application...")
    await close_db_connection()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Multi-user todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent JSON response format."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with clear error messages."""
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error", "errors": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with generic error message."""
    logger.error(f"Unexpected error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Service status

    Example:
        GET /health

        Response (200):
        {
            "status": "ok",
            "message": "Todo API is running"
        }
    """
    return {
        "status": "ok",
        "message": "Todo API is running"
    }


@app.get("/", tags=["Health"])
async def root():
    """
    API information endpoint.

    Returns:
        dict: API version and documentation links

    Example:
        GET /

        Response (200):
        {
            "message": "Todo API v1.0.0",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health"
        }
    """
    return {
        "message": "Todo API v1.0.0",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
