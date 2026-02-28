from datetime import datetime
from config import TRANSCRIPT_FILE
from logger import get_logger

logger = get_logger(__name__)


def init_transcript():
    """Create a fresh transcript file with a header."""
    try:
        with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"AI Discussion Stream — started {timestamp}\n")
            f.write("=" * 50 + "\n\n")
        logger.info(f"Transcript initialized: {TRANSCRIPT_FILE}")
    except PermissionError as e:
        logger.error(f"Permission denied creating transcript file {TRANSCRIPT_FILE}: {e}")
    except OSError as e:
        logger.error(f"File system error creating transcript file {TRANSCRIPT_FILE}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error creating transcript file: {e}")


def log_message(agent_name: str, text: str, topic: str | None = None):
    """
    Append a single message to the transcript.
    Optionally logs a topic change marker.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    try:
        with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
            if topic:
                f.write(f"\n📚 [{timestamp}] — Topic: {topic}\n\n")
            if text:  # Only write message if text is not empty
                f.write(f"[{timestamp}] {agent_name}: {text}\n")
        logger.debug(f"Transcript updated: {agent_name}")
    except PermissionError as e:
        logger.error(f"Permission denied writing to transcript file: {e}")
    except OSError as e:
        logger.error(f"File system error writing to transcript file: {e}")
    except UnicodeEncodeError as e:
        # Skip problematic characters and continue
        logger.warning(f"Encoding error in transcript (skipping problematic characters): {e}")
        try:
            # Retry with error handling for encoding issues
            with open(TRANSCRIPT_FILE, "a", encoding="utf-8", errors="ignore") as f:
                if topic:
                    f.write(f"\n📚 [{timestamp}] — Topic: {topic}\n\n")
                if text:
                    f.write(f"[{timestamp}] {agent_name}: {text}\n")
        except Exception as retry_error:
            logger.error(f"Failed to write transcript even with error handling: {retry_error}")
    except Exception as e:
        logger.error(f"Unexpected error writing to transcript: {e}")
