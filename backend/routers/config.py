"""
Configuration management API endpoints.

Provides REST API endpoints for:
- Getting agent configurations
- Getting available topics
- Updating stream configuration
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List
from backend.models.schemas import AgentConfig, ConfigUpdate, ConfigUpdateResponse
from logger import get_logger
import config as app_config

logger = get_logger(__name__)
router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("/agents", response_model=Dict[str, AgentConfig])
async def get_agents():
    """
    Get all agent configurations.

    Returns a dictionary mapping agent keys to their full configuration,
    including voice IDs, colors, and system prompts.
    """
    logger.debug("API request: get agents")

    agents_response = {}
    for key, agent_data in app_config.AGENTS.items():
        agents_response[key] = AgentConfig(**agent_data)

    return agents_response


@router.get("/topics", response_model=List[str])
async def get_topics():
    """
    Get available discussion topics.

    Returns a list of all topics that can be used for AI discussions.
    """
    logger.debug("API request: get topics")
    return app_config.TOPICS


@router.get("/settings")
async def get_settings():
    """
    Get current stream settings.

    Returns all configurable settings like max_turns, pause_between_turns, etc.
    """
    logger.debug("API request: get settings")

    return {
        "max_turns": app_config.MAX_TURNS,
        "pause_between_turns": app_config.PAUSE_BETWEEN_TURNS,
        "topic_switch_every": app_config.TOPIC_SWITCH_EVERY,
        "context_window": app_config.CONTEXT_WINDOW,
        "groq_model": app_config.GROQ_MODEL,
        "audio_dir": app_config.AUDIO_DIR,
        "chars_per_second": app_config.CHARS_PER_SECOND
    }


@router.put("/", response_model=ConfigUpdateResponse)
async def update_config(config_update: ConfigUpdate):
    """
    Update stream configuration.

    Updates are applied to the config module and will affect the next stream run.
    Does NOT affect currently running streams.

    - **max_turns**: Default number of turns for new streams
    - **pause_between_turns**: Pause duration in seconds between turns
    - **topics**: List of available discussion topics
    """
    logger.info(f"API request: update config - {config_update.dict(exclude_none=True)}")

    updated_fields = []

    # Update max_turns
    if config_update.max_turns is not None:
        app_config.MAX_TURNS = config_update.max_turns
        updated_fields.append("max_turns")

    # Update pause_between_turns
    if config_update.pause_between_turns is not None:
        app_config.PAUSE_BETWEEN_TURNS = config_update.pause_between_turns
        updated_fields.append("pause_between_turns")

    # Update topics
    if config_update.topics is not None:
        if len(config_update.topics) < 1:
            raise HTTPException(
                status_code=400,
                detail="At least one topic is required"
            )
        app_config.TOPICS = config_update.topics
        updated_fields.append("topics")

    if not updated_fields:
        return ConfigUpdateResponse(
            success=False,
            message="No fields provided to update",
            updated_fields=[]
        )

    logger.info(f"Configuration updated: {updated_fields}")

    return ConfigUpdateResponse(
        success=True,
        message=f"Updated {len(updated_fields)} field(s): {', '.join(updated_fields)}",
        updated_fields=updated_fields
    )
