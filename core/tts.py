import os
import platform
import time
import subprocess
from core.avatar import set_avatar
from elevenlabs.client import ElevenLabs
from elevenlabs.core import ApiError as ElevenLabsAPIError
from config import ELEVENLABS_API_KEY, AGENTS, AUDIO_DIR, CHARS_PER_SECOND
from utils.retry import retry_with_backoff
from logger import get_logger

logger = get_logger(__name__)

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


@retry_with_backoff(max_retries=3, base_delay=1, exceptions=(Exception,))
def text_to_speech(text: str, agent_key: str, filename: str) -> bool:
    """
    Convert text to an audio file using ElevenLabs.
    Returns True if successful, False otherwise.

    Includes retry logic with exponential backoff for API failures.
    """
    agent = AGENTS[agent_key]
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        logger.debug(f"Converting text to speech for {agent['name']}: {len(text)} chars")

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

        # Validate audio file was created successfully
        if not os.path.exists(filepath):
            logger.error(f"Audio file not created: {filepath}")
            return False

        file_size = os.path.getsize(filepath)
        logger.info(f"Audio saved: {filename} ({file_size} bytes)")
        return True

    except ElevenLabsAPIError as e:
        # Check if quota exceeded
        if "quota" in str(e).lower():
            logger.error(f"ElevenLabs quota exceeded: {e}")
            return False
        logger.error(f"ElevenLabs API error for {agent['name']}: {e}")
        raise  # Let retry decorator handle other API errors

    except OSError as e:
        logger.critical(f"File system error writing audio file {filepath}: {e}")
        return False

    except Exception as e:
        logger.error(f"TTS error for {agent['name']}: {e}")
        raise  # Let retry decorator handle it


def play_audio(filename: str, agent_key: str, text: str) -> float:
    """
    Play an audio file AND animate avatar mouth simultaneously.
    Works on macOS, Windows, Linux.
    """
    filepath = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(filepath):
        logger.warning(f"Audio file not found: {filepath}")
        return 0.0

    duration = estimate_duration(text)
    logger.debug(f"Playing audio: {filename} (estimated {duration:.1f}s)")

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
        logger.debug(f"Audio playback completed: {filename}")
    except Exception as e:
        logger.error(f"Playback error for {filename}: {e}")

    # Stop mouth animation
    stop_animation.set()
    t.join(timeout=0.5)

    return duration


def estimate_duration(text: str) -> float:
    """Rough estimate of how long the audio will be based on character count."""
    return len(text) / CHARS_PER_SECOND
