"""
StreamManager service for managing AI discussion stream lifecycle.

This is a singleton service that:
- Manages stream state (running/stopped)
- Runs streams in background threads
- Broadcasts transcript updates to WebSocket clients
- Ensures only one stream runs at a time
"""

import asyncio
import threading
import time
import random
import os
from queue import Queue  # Thread-safe queue for async/sync communication
from typing import Optional, List, Dict
from datetime import datetime

from logger import get_logger
from config import AGENTS, TOPICS, AUDIO_DIR, MAX_TURNS, TOPIC_SWITCH_EVERY, PAUSE_BETWEEN_TURNS
from core.dialogue import generate_response, reset_history
from core.tts import text_to_speech, play_audio
from core.overlay import update_overlay
from core.transcript import init_transcript, log_message, set_broadcast_callback
from core.avatar import connect as connect_obs, set_avatar, set_both_idle, start_idle_animation, stop_idle_animation

logger = get_logger(__name__)


class StreamManager:
    """Singleton service to manage AI stream lifecycle."""

    _instance: Optional['StreamManager'] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.is_running = False
        self.current_turn = 0
        self.current_topic = ""
        self.max_turns = MAX_TURNS
        self.errors: List[str] = []
        self.stream_thread: Optional[threading.Thread] = None
        self.stop_flag = threading.Event()

        # Thread-safe queue for passing transcript messages from sync thread to async WebSocket handlers
        self.transcript_queue: Queue = Queue()

        # Set up transcript broadcasting
        set_broadcast_callback(self.broadcast_transcript)

        logger.info("StreamManager initialized")

    def start_stream(self, max_turns: int = 5) -> Dict[str, any]:
        """
        Start the AI discussion stream in a background thread.

        Args:
            max_turns: Number of turns to run

        Returns:
            Dict with success status and message
        """
        with self._lock:
            if self.is_running:
                logger.warning("Attempted to start stream while already running")
                return {
                    "success": False,
                    "message": "Stream is already running",
                    "status": self.get_status()
                }

            self.max_turns = max_turns
            self.current_turn = 0
            self.current_topic = ""
            self.errors = []
            self.stop_flag.clear()
            self.is_running = True

            # Start stream in background thread
            self.stream_thread = threading.Thread(target=self._run_stream, daemon=True)
            self.stream_thread.start()

            logger.info(f"Stream started with max_turns={max_turns}")
            return {
                "success": True,
                "message": f"Stream started successfully with {max_turns} turns",
                "status": self.get_status()
            }

    def stop_stream(self) -> Dict[str, any]:
        """
        Stop the running stream gracefully.

        Returns:
            Dict with success status and message
        """
        with self._lock:
            if not self.is_running:
                logger.warning("Attempted to stop stream that is not running")
                return {
                    "success": False,
                    "message": "No stream is currently running"
                }

            self.stop_flag.set()
            logger.info("Stream stop requested")

            return {
                "success": True,
                "message": "Stream stopping..."
            }

    def get_status(self) -> Dict[str, any]:
        """
        Get current stream status.

        Returns:
            Dict with stream status information
        """
        return {
            "is_running": self.is_running,
            "current_turn": self.current_turn,
            "current_topic": self.current_topic,
            "max_turns": self.max_turns,
            "errors": self.errors[-10:]  # Last 10 errors
        }

    def broadcast_transcript(self, message: Dict):
        """
        Send transcript message to WebSocket clients via thread-safe queue.

        Called from the stream thread (sync context). Messages are placed in a
        queue and consumed by async WebSocket handlers.

        Args:
            message: Dict with timestamp, agent_name, text, topic
        """
        # Add turn number to message
        message["turn"] = self.current_turn

        # Put message in thread-safe queue for async WebSocket handlers to consume
        try:
            self.transcript_queue.put_nowait(message)
            logger.debug(f"Queued transcript message from {message.get('agent_name', 'system')}")
        except Exception as e:
            logger.error(f"Error queuing transcript message: {e}")

    def _run_stream(self):
        """
        Main stream loop (runs in background thread).
        This is the core logic from main.py adapted for threaded execution.
        """
        try:
            logger.info("Stream thread started")
            start_time = datetime.now()
            successful_turns = 0
            failed_turns = 0

            # Ensure directories exist
            os.makedirs(AUDIO_DIR, exist_ok=True)

            # Fresh transcript
            init_transcript()

            # Connect to OBS
            connect_obs()
            set_both_idle()

            # Start idle animations
            start_idle_animation("agent1")
            start_idle_animation("agent2")

            # Pick starting topic
            self.current_topic = random.choice(TOPICS)
            logger.info(f"Starting topic: {self.current_topic}")

            # Opening line
            opening_text = (
                f"Welcome, everyone! Today we're going to explore a fascinating question: "
                f"{self.current_topic} Let's dive in."
            )

            audio_file = "opening.mp3"
            if text_to_speech(opening_text, "agent1", audio_file):
                update_overlay("agent1", opening_text, self.current_topic)
                log_message(AGENTS["agent1"]["name"], opening_text, topic=self.current_topic)
                play_audio(audio_file, "agent1", opening_text)
                time.sleep(PAUSE_BETWEEN_TURNS)
            else:
                logger.warning("Failed to generate opening audio, continuing anyway")

            # Main loop
            for turn in range(self.max_turns):
                # Check stop flag
                if self.stop_flag.is_set():
                    logger.info("Stream stopped by user request")
                    break

                try:
                    self.current_turn = turn + 1

                    # Alternate speakers
                    agent_key = "agent2" if turn % 2 == 0 else "agent1"
                    agent = AGENTS[agent_key]

                    logger.info(f"Turn {turn + 1}/{self.max_turns}: {agent['name']} thinking...")

                    # Generate reply
                    text = generate_response(agent_key, self.current_topic)

                    # Speech
                    audio_file = f"turn_{turn}.mp3"
                    success = text_to_speech(text, agent_key, audio_file)
                    if not success:
                        logger.warning(f"Turn {turn + 1} skipped - TTS failed")
                        failed_turns += 1
                        self.errors.append(f"Turn {turn + 1}: TTS failed")
                        continue

                    # Overlay + transcript
                    update_overlay(agent_key, text, self.current_topic)
                    log_message(agent["name"], text)

                    # Play audio
                    logger.info(f"{agent['name']}: {text}")
                    play_audio(audio_file, agent_key, text)

                    successful_turns += 1

                    # Pause
                    time.sleep(PAUSE_BETWEEN_TURNS)

                    # Topic switch
                    if (turn + 1) % TOPIC_SWITCH_EVERY == 0 and turn < self.max_turns - 2:
                        self.current_topic = random.choice(
                            [t for t in TOPICS if t != self.current_topic]
                        )
                        reset_history()
                        logger.info(f"Topic switched to: {self.current_topic}")
                        log_message("", "", topic=self.current_topic)
                        time.sleep(1)

                except Exception as e:
                    logger.error(f"Error in turn {turn + 1}: {e}", exc_info=True)
                    failed_turns += 1
                    self.errors.append(f"Turn {turn + 1}: {str(e)}")

            # Stop idle animation
            stop_idle_animation()

            # Summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            success_rate = (successful_turns / self.max_turns * 100) if self.max_turns > 0 else 0

            logger.info("=" * 60)
            logger.info("Stream finished!")
            logger.info(f"Duration: {duration:.1f}s")
            logger.info(f"Successful turns: {successful_turns}/{self.max_turns} ({success_rate:.1f}%)")
            logger.info(f"Failed turns: {failed_turns}")
            logger.info("=" * 60)

        except Exception as e:
            logger.critical(f"Fatal error in stream thread: {e}", exc_info=True)
            self.errors.append(f"Fatal: {str(e)}")
        finally:
            with self._lock:
                self.is_running = False
                self.current_turn = 0
            logger.info("Stream thread ended")
