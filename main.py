import os
import time
import random

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


def main():
    # ── Ensure directories exist ──────────────────────
    os.makedirs(AUDIO_DIR, exist_ok=True)

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
    print("\n" + "=" * 55)
    print("  🎙️  AI Avatar Discussion Stream")
    print("=" * 55)
    print(f"  📚 Starting topic: {current_topic}\n")

    # ── Opening line (agent1 introduces the topic) ───
    opening_text = (
        f"Welcome, everyone! Today we're going to explore a fascinating question: "
        f"{current_topic} Let's dive in."
    )

    audio_file = "opening.mp3"
    text_to_speech(opening_text, "agent1", audio_file)
    update_overlay("agent1", opening_text, current_topic)
    log_message(AGENTS["agent1"]["name"], opening_text, topic=current_topic)

    print(f"🗣️  {AGENTS['agent1']['name']}: {opening_text}\n")
    play_audio(audio_file, "agent1", opening_text)  # plays audio AND animates mouth
    time.sleep(PAUSE_BETWEEN_TURNS)

    # ── Main loop ─────────────────────────────────────
    for turn in range(MAX_TURNS):
        # Alternate speakers: even turns → agent2, odd → agent1
        agent_key = "agent2" if turn % 2 == 0 else "agent1"
        agent     = AGENTS[agent_key]

        print(f"💭 {agent['name']} is thinking...")

        # 1. Generate reply
        text = generate_response(agent_key, current_topic)

        # 2. Speech
        audio_file = f"turn_{turn}.mp3"
        success = text_to_speech(text, agent_key, audio_file)
        if not success:
            print("  ⚠️  Skipping turn — TTS failed.\n")
            continue

        # 3. Overlay + transcript
        update_overlay(agent_key, text, current_topic)
        log_message(agent["name"], text)

        # 4. Print + play
        print(f"🗣️  {agent['name']}: {text}\n")
        play_audio(audio_file, agent_key, text)  # plays audio AND animates mouth

        # Wait for a short pause (audio already finished - afplay is blocking)
        time.sleep(PAUSE_BETWEEN_TURNS)

        # ── Topic switch every N turns ──────────────
        if (turn + 1) % TOPIC_SWITCH_EVERY == 0 and turn < MAX_TURNS - 2:
            current_topic = random.choice(
                [t for t in TOPICS if t != current_topic]
            )
            reset_history()  # fresh context for the new topic
            print(f"\n📚 Switching topic → {current_topic}\n")
            log_message("", "", topic=current_topic)
            time.sleep(1)

    # ── Stop idle animation ──────────────────────────
    from avatar import stop_idle_animation
    stop_idle_animation()

    # ── Done ──────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  ✅ Discussion finished! Check transcript.txt")
    print("=" * 55)


if __name__ == "__main__":
    main()
