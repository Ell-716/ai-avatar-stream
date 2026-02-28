import os
import time
import random
from datetime import datetime

from config import (
    AGENTS,
    TOPICS,
    AUDIO_DIR,
    MAX_TURNS,
    TOPIC_SWITCH_EVERY,
    PAUSE_BETWEEN_TURNS,
)
from dialogue import generate_response, reset_history
from tts import text_to_speech, play_audio, estimate_duration
from overlay import update_overlay
from transcript import init_transcript, log_message
from avatar import connect as connect_obs, set_avatar, set_both_idle
from logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Main entry point for the AI avatar discussion stream.

    Orchestrates the entire conversation flow, including:
    - Setting up directories and connections
    - Generating responses from agents
    - Converting text to speech
    - Animating avatars
    - Managing topic switches
    """
    start_time = datetime.now()
    successful_turns = 0
    failed_turns = 0

    try:
        logger.info("=" * 60)
        logger.info("AI Avatar Discussion Stream - Starting")
        logger.info("=" * 60)

        # ── Ensure directories exist ──────────────────────
        os.makedirs(AUDIO_DIR, exist_ok=True)
        logger.debug(f"Audio directory ready: {AUDIO_DIR}")

        # ── Fresh transcript ──────────────────────────────
        init_transcript()

        # ── Connect to OBS for avatar swapping ───────────
        connect_obs()
        set_both_idle()

        # Start subtle idle motion for both avatars
        from avatar import start_idle_animation
        start_idle_animation("agent1")
        start_idle_animation("agent2")

        # ── Pick a starting topic ─────────────────────────
        current_topic = random.choice(TOPICS)
        logger.info(f"Starting topic: {current_topic}")

        # ── Opening line (agent1 introduces the topic) ───
        opening_text = (
            f"Welcome, everyone! Today we're going to explore a fascinating question: "
            f"{current_topic} Let's dive in."
        )

        audio_file = "opening.mp3"
        logger.info(f"{AGENTS['agent1']['name']}: {opening_text}")

        if text_to_speech(opening_text, "agent1", audio_file):
            update_overlay("agent1", opening_text, current_topic)
            log_message(AGENTS["agent1"]["name"], opening_text, topic=current_topic)
            play_audio(audio_file, "agent1", opening_text)
            time.sleep(PAUSE_BETWEEN_TURNS)
        else:
            logger.warning("Failed to generate opening audio, continuing anyway")

        # ── Main loop ─────────────────────────────────────
        for turn in range(MAX_TURNS):
            try:
                # Alternate speakers: even turns → agent2, odd → agent1
                agent_key = "agent2" if turn % 2 == 0 else "agent1"
                agent     = AGENTS[agent_key]

                logger.info(f"Turn {turn + 1}/{MAX_TURNS}: {agent['name']} thinking...")

                # 1. Generate reply
                text = generate_response(agent_key, current_topic)

                # 2. Speech
                audio_file = f"turn_{turn}.mp3"
                success = text_to_speech(text, agent_key, audio_file)
                if not success:
                    logger.warning(f"Turn {turn + 1} skipped - TTS failed")
                    failed_turns += 1
                    continue

                # 3. Overlay + transcript
                update_overlay(agent_key, text, current_topic)
                log_message(agent["name"], text)

                # 4. Print + play
                logger.info(f"{agent['name']}: {text}")
                play_audio(audio_file, agent_key, text)

                successful_turns += 1

                # Wait for a short pause (audio already finished - afplay is blocking)
                time.sleep(PAUSE_BETWEEN_TURNS)

                # ── Topic switch every N turns ──────────────
                if (turn + 1) % TOPIC_SWITCH_EVERY == 0 and turn < MAX_TURNS - 2:
                    current_topic = random.choice(
                        [t for t in TOPICS if t != current_topic]
                    )
                    reset_history()
                    logger.info(f"Topic switched to: {current_topic}")
                    log_message("", "", topic=current_topic)
                    time.sleep(1)

            except KeyboardInterrupt:
                logger.warning("Stream interrupted by user")
                raise
            except Exception as e:
                logger.error(f"Error in turn {turn + 1}: {e}", exc_info=True)
                failed_turns += 1
                # Continue to next turn instead of crashing

        # ── Stop idle animation ──────────────────────────
        from avatar import stop_idle_animation
        stop_idle_animation()

        # ── Summary statistics ──────────────────────────
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        success_rate = (successful_turns / MAX_TURNS * 100) if MAX_TURNS > 0 else 0

        logger.info("=" * 60)
        logger.info("Discussion finished!")
        logger.info(f"Duration: {duration:.1f}s")
        logger.info(f"Successful turns: {successful_turns}/{MAX_TURNS} ({success_rate:.1f}%)")
        logger.info(f"Failed turns: {failed_turns}")
        logger.info(f"Transcript saved to: transcript.txt")
        logger.info("=" * 60)

    except KeyboardInterrupt:
        logger.info("Stream stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error in main loop: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
