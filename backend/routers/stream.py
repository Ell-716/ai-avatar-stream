"""
Stream control API endpoints.

Provides REST API endpoints for:
- Starting streams
- Stopping streams
- Getting stream status
"""

from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    StreamStatus,
    StreamStartRequest,
    StreamStartResponse,
    StreamStopRequest,
    StreamStopResponse
)
from backend.services.stream_manager import StreamManager
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/stream", tags=["stream"])

# Get singleton instance
stream_manager = StreamManager()


@router.post("/start", response_model=StreamStartResponse)
async def start_stream(request: StreamStartRequest):
    """
    Start the AI discussion stream.

    - **max_turns**: Number of conversation turns to run (1-100)

    Returns success/failure status and current stream state.

    Raises 409 Conflict if a stream is already running.
    """
    logger.info(f"API request: start stream with max_turns={request.max_turns}")

    result = stream_manager.start_stream(max_turns=request.max_turns)

    if not result["success"]:
        raise HTTPException(status_code=409, detail=result["message"])

    return StreamStartResponse(
        success=True,
        message=result["message"],
        status=StreamStatus(**result["status"])
    )


@router.post("/stop", response_model=StreamStopResponse)
async def stop_stream(request: StreamStopRequest):
    """
    Stop the currently running stream.

    Stops the stream gracefully, allowing the current turn to complete.

    Raises 400 Bad Request if no stream is running.
    """
    logger.info("API request: stop stream")

    result = stream_manager.stop_stream()

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return StreamStopResponse(
        success=True,
        message=result["message"]
    )


@router.get("/status", response_model=StreamStatus)
async def get_status():
    """
    Get current stream status.

    Returns:
    - Whether stream is running
    - Current turn number
    - Current discussion topic
    - Maximum turns
    - Recent errors (last 10)
    """
    logger.debug("API request: get stream status")

    status = stream_manager.get_status()
    return StreamStatus(**status)
