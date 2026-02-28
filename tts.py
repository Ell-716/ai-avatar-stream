import os
import platform
import time
import subprocess
from avatar import set_avatar
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, AGENTS, AUDIO_DIR, CHARS_PER_SECOND

def animate_mouth(agent_key: str, duration: float):
    """
    Cycle mouth states during speech to simulate talking.
    """
    states = ["small", "medium", "small", "large"]
    start = time.time()
    i = 0

    while time.time() - start < duration:
        set_avatar(agent_key, states[i % len(states)])
        time.sleep(0.12)
        i += 1

    set_avatar(agent_key, "idle")


client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def text_to_speech(text: str, agent_key: str, filename: str) -> bool:
    """
    Convert text to an audio file using ElevenLabs.
    Returns True if successful, False otherwise.
    """
    agent = AGENTS[agent_key]
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        audio_generator = client.text_to_speech.convert(
            voice_id=agent["voice_id"],
            text=text,
            model_id="eleven_turbo_v2_5"
        )

        # Collect audio bytes from the iterator
        audio_bytes = b''.join(audio_generator)

        # Write to file
        with open(filepath, 'wb') as f:
            f.write(audio_bytes)

        print(f"  🎵 Audio saved: {filepath}")
        return True

    except Exception as e:
        print(f"  ❌ TTS Error: {e}")
        return False


def play_audio(filename: str, agent_key: str, text: str) -> float:
    """
    Play an audio file AND animate avatar mouth simultaneously.
    Works on macOS, Windows, Linux.
    """
    filepath = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(filepath):
        print(f"  ⚠️  Audio file not found: {filepath}")
        return 0.0

    duration = estimate_duration(text)

    # Thread for mouth animation
    import threading
    stop_animation = threading.Event()

    def mouth_loop():
        states = ["small", "medium", "small"]
        i = 0
        while not stop_animation.is_set():
            set_avatar(agent_key, states[i % len(states)])
            i += 1
            time.sleep(0.12)
        set_avatar(agent_key, "idle")

    t = threading.Thread(target=mouth_loop)
    t.start()

    # Play audio (blocking)
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.call(["afplay", filepath])
        elif system == "Windows":
            subprocess.Popen(["start", "/b", filepath], shell=True).wait()
        else:
            subprocess.call(["ffplay", "-nodisp", "-autoexit", filepath])
    except Exception as e:
        print(f"  ❌ Playback error: {e}")

    # Stop mouth animation
    stop_animation.set()
    t.join(timeout=0.5)

    return duration


def estimate_duration(text: str) -> float:
    """Rough estimate of how long the audio will be based on character count."""
    return len(text) / CHARS_PER_SECOND
