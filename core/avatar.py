"""
avatar.py — controls avatar image swapping in OBS via WebSocket
using multiple mouth states (idle / small / medium / large).

How it works:
    1. Connects to OBS via obs-websocket
    2. Sets avatar image based on mouth state
    3. Used by dialogue / TTS logic to animate avatars

Requires:
    - OBS WebSocket plugin enabled
    - pip install obs-websocket-py
"""

from obswebsocket import obsws, requests as obs_requests
from obswebsocket.exceptions import ConnectionFailure
from config import AGENTS
from logger import get_logger
import os
import threading
import time

logger = get_logger(__name__)

# OBS WebSocket connection
ws = None


def connect(max_retries: int = 3, retry_delay: float = 2.0):
    """
    Connect to OBS WebSocket. Call once at startup.

    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay between retry attempts in seconds
    """
    global ws

    for attempt in range(max_retries):
        try:
            ws = obsws("127.0.0.1", 4455, "")  # host, port, password
            ws.connect()
            logger.info("Connected to OBS via WebSocket")
            return
        except ConnectionFailure as e:
            if attempt < max_retries - 1:
                logger.warning(
                    f"OBS WebSocket connection failed (attempt {attempt + 1}/{max_retries}): {e}. "
                    f"Retrying in {retry_delay}s..."
                )
                time.sleep(retry_delay)
            else:
                logger.warning(
                    f"Could not connect to OBS WebSocket after {max_retries} attempts: {e}. "
                    "Avatar swapping will be disabled."
                )
                ws = None
        except Exception as e:
            logger.error(f"Unexpected error connecting to OBS WebSocket: {e}")
            ws = None
            return


def set_avatar(agent_key: str, mouth: str):
    """
    Set avatar image in OBS based on mouth state.

    agent_key: "agent1" | "agent2"
    mouth: "idle" | "small" | "medium"
    """
    if ws is None:
        # WebSocket not connected - skip silently at DEBUG level
        logger.debug(f"Skipping avatar swap for {agent_key} (WebSocket not connected)")
        return

    agent = AGENTS.get(agent_key)
    if agent is None:
        logger.error(f"Invalid agent key: {agent_key}")
        return

    source_name = agent["name"]

    if mouth == "idle":
        image_path = agent["avatar_idle"]
    elif mouth == "small":
        image_path = agent["avatar_talk_small"]
    elif mouth == "medium":
        image_path = agent["avatar_talk_medium"]
    else:
        logger.warning(f"Invalid mouth state '{mouth}' for {agent_key}")
        return

    try:
        abs_path = os.path.abspath(image_path)
        ws.call(
            obs_requests.SetInputSettings(
                inputName=source_name,
                inputSettings={"file": abs_path},
                overlay=True,
            )
        )
        logger.debug(f"Avatar swapped: {agent_key} → {mouth}")

    except Exception as e:
        error_msg = str(e)
        if "No source" in error_msg or "not found" in error_msg.lower():
            logger.error(f"OBS source not found: '{source_name}'. Check OBS scene configuration.")
        else:
            logger.warning(f"Avatar swap failed for {agent_key}: {e}")


def set_both_idle():
    """Set both avatars to idle state."""
    set_avatar("agent1", "idle")
    set_avatar("agent2", "idle")


_idle_thread_running = False

def start_idle_animation(agent_key: str, interval: float = 0.8, movement: int = 2):
    """
    Animate small idle motion for an avatar (up/down) in a separate thread.
    agent_key: "agent1" or "agent2"
    interval: seconds between movements
    movement: pixel offset (for overlay, scale, or ignore if simple image swap)
    """
    global _idle_thread_running
    if _idle_thread_running:
        logger.debug(f"Idle animation already running for {agent_key}")
        return

    _idle_thread_running = True
    logger.debug(f"Starting idle animation for {agent_key}")

    def idle_loop():
        toggle = True
        while _idle_thread_running:
            # For simple PNG swap, you could flash between idle images or just do nothing
            # Here we simply call idle to ensure image stays visible
            set_avatar(agent_key, "idle")
            # Could add tiny movement in OBS with WebSocket Transform if desired
            time.sleep(interval)
            toggle = not toggle

    t = threading.Thread(target=idle_loop, daemon=True)
    t.start()


def stop_idle_animation():
    """Stop all idle animations."""
    global _idle_thread_running
    _idle_thread_running = False
    logger.debug("Stopped idle animations")
