from datetime import datetime
from config import TRANSCRIPT_FILE


def init_transcript():
    """Create a fresh transcript file with a header."""
    with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"AI Discussion Stream — started {timestamp}\n")
        f.write("=" * 50 + "\n\n")


def log_message(agent_name: str, text: str, topic: str | None = None):
    """
    Append a single message to the transcript.
    Optionally logs a topic change marker.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
        if topic:
            f.write(f"\n📚 [{timestamp}] — Topic: {topic}\n\n")
        f.write(f"[{timestamp}] {agent_name}: {text}\n")
