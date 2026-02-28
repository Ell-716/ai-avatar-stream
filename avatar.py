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
from config import AGENTS
import os
import threading
import time

# OBS WebSocket connection
ws = None


def connect():
    """Connect to OBS WebSocket. Call once at startup."""
    global ws
    try:
        ws = obsws("127.0.0.1", 4455, "")  # host, port, password
        ws.connect()
        print("✅ Connected to OBS via WebSocket")
    except Exception as e:
        print(f"⚠️  Could not connect to OBS WebSocket: {e}")
        print("   Avatar swapping will be disabled.")
        ws = None


def set_avatar(agent_key: str, mouth: str):
    """
    Set avatar image in OBS based on mouth state.

    agent_key: "agent1" | "agent2"
    mouth: "idle" | "small" | "medium"
    """
    if ws is None:
        return

    agent = AGENTS.get(agent_key)
    if agent is None:
        return

    source_name = agent["name"]

    if mouth == "idle":
        image_path = agent["avatar_idle"]
    elif mouth == "small":
        image_path = agent["avatar_talk_small"]
    elif mouth == "medium":
        image_path = agent["avatar_talk_medium"]
    else:
        return  # invalid mouth state

    try:
        abs_path = os.path.abspath(image_path)
        ws.call(
            obs_requests.SetInputSettings(
                inputName=source_name,
                inputSettings={"file": abs_path},
                overlay=True,
            )
        )
    except Exception as e:
        print(f"⚠️ Avatar swap failed for {agent_key}: {e}")


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
        return

    _idle_thread_running = True

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
