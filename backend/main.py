"""
FastAPI backend for the AI Avatar Stream.

Provides REST API and WebSocket endpoints for controlling and monitoring
the AI discussion stream programmatically.

Run with:
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

API documentation available at:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import stream, config
from backend.websockets import transcript
from backend.models.schemas import HealthResponse
from logger import get_logger
import uvicorn

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Avatar Stream API",
    description="REST API and WebSocket interface for AI discussion streams",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Create React App default
        "http://localhost:5173",      # Vite default
        "http://localhost:5174",      # Alternative Vite port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stream.router)
app.include_router(config.router)
app.include_router(transcript.router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("=" * 60)
    logger.info("AI Avatar Stream API - Starting")
    logger.info("=" * 60)
    logger.info("Swagger UI: http://localhost:8000/docs")
    logger.info("ReDoc: http://localhost:8000/redoc")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("AI Avatar Stream API - Shutting down")


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "AI Avatar Stream API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    """
    Health check endpoint.

    Returns the current health status of the API.
    """
    return HealthResponse(status="healthy", version="1.0.0")


if __name__ == "__main__":
    # Run with: python -m backend.main
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
