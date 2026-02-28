"""
Pydantic models for API request/response validation.

Defines all data structures used by the FastAPI endpoints for
request validation and response serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class StreamStatus(BaseModel):
    """Current status of the AI discussion stream."""
    is_running: bool = Field(..., description="Whether the stream is currently running")
    current_turn: int = Field(..., description="Current turn number (0 if not running)")
    current_topic: str = Field(..., description="Current discussion topic")
    max_turns: int = Field(..., description="Maximum number of turns for this stream")
    errors: List[str] = Field(default_factory=list, description="Recent errors")


class StreamStartRequest(BaseModel):
    """Request to start a new stream."""
    max_turns: Optional[int] = Field(default=5, ge=1, le=100, description="Number of turns to run")


class StreamStartResponse(BaseModel):
    """Response after starting a stream."""
    success: bool
    message: str
    status: Optional[StreamStatus] = None


class StreamStopRequest(BaseModel):
    """Request to stop the current stream."""
    pass


class StreamStopResponse(BaseModel):
    """Response after stopping a stream."""
    success: bool
    message: str


class AgentConfig(BaseModel):
    """Configuration for a single AI agent."""
    name: str = Field(..., description="Display name of the agent")
    voice_id: str = Field(..., description="ElevenLabs voice ID")
    color: str = Field(..., description="Color code for UI display (hex)")
    system_prompt: str = Field(..., description="System prompt defining agent personality")
    avatar_idle: Optional[str] = Field(None, description="Path to idle avatar image")
    avatar_talk_small: Optional[str] = Field(None, description="Path to small mouth avatar")
    avatar_talk_medium: Optional[str] = Field(None, description="Path to medium mouth avatar")


class ConfigUpdate(BaseModel):
    """Request to update stream configuration."""
    max_turns: Optional[int] = Field(None, ge=1, le=100, description="Default number of turns")
    pause_between_turns: Optional[float] = Field(None, ge=0, le=10, description="Pause duration in seconds")
    topics: Optional[List[str]] = Field(None, description="Available discussion topics")


class ConfigUpdateResponse(BaseModel):
    """Response after updating configuration."""
    success: bool
    message: str
    updated_fields: List[str]


class TranscriptMessage(BaseModel):
    """A single message in the transcript."""
    timestamp: str = Field(..., description="ISO format timestamp")
    agent_name: str = Field(..., description="Name of the speaking agent")
    text: str = Field(..., description="The message content")
    topic: Optional[str] = Field(None, description="Discussion topic (if this is a topic change)")
    turn: Optional[int] = Field(None, description="Turn number")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"
