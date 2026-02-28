import os
from dotenv import load_dotenv

load_dotenv()

# ─── API Keys ────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ─── Groq Model ──────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"

# ─── Conversation Settings ──────────────────────────────
MAX_TURNS = 5                  # Total turns before stream ends
CONTEXT_WINDOW = 6              # How many past messages agents remember
TOPIC_SWITCH_EVERY = 8          # Switch topic every N turns
PAUSE_BETWEEN_TURNS = 1         # Seconds of silence between turns
CHARS_PER_SECOND = 15           # Estimate for audio duration calculation

# ─── File Paths ──────────────────────────────────────────
AUDIO_DIR = "audio"
AVATARS_DIR = "avatars"
DIALOGUE_HTML = "dialogue.html"
TRANSCRIPT_FILE = "transcript.txt"

# ─── Agents ──────────────────────────────────────────────
AGENTS = {
    "agent1": {
        "name": "Dr. Elena",
        "voice_id": os.getenv("VOICE_ID_ELENA", "21m00Tcm4TlvDq8ikWAM"),
        "avatar_idle": "avatars/agent1.png",
        "avatar_talk_small": "avatars/agent1_talk_small.png",
        "avatar_talk_medium": "avatars/agent1_talk_medium.png",
        "color": "#00ff88",
        "system_prompt": (
            "You are Dr. Elena, an optimistic molecular biologist. "
            "You believe aging can be reversed with the right interventions. "
            "You reference recent research and are enthusiastic about longevity science. "
            "Keep responses to 1-2 sentences. Be conversational and natural."
        ),
    },
    "agent2": {
        "name": "Prof. Marcus",
        "voice_id": os.getenv("VOICE_ID_MARCUS", "29vD33N1CtxCmqQRPOHJ"),
        "avatar_idle": "avatars/agent2.png",
        "avatar_talk_small": "avatars/agent2_talk_small.png",
        "avatar_talk_medium": "avatars/agent2_talk_medium.png",
        "color": "#ff6b6b",
        "system_prompt": (
            "You are Prof. Marcus, a cautious gerontologist. "
            "You're skeptical of anti-aging hype and always ask for evidence. "
            "You point out flaws in reasoning but remain respectful. "
            "Keep responses to 1-2 sentences. Be thoughtful and measured."
        ),
    },
}

# ─── Discussion Topics ──────────────────────────────────
TOPICS = [
    "Why do different organs age at different rates?",
    "Are epigenetic clocks accurate for measuring biological age?",
    "Can caloric restriction really extend lifespan in humans?",
    "What's the role of senescent cells in aging?",
    "Is aging a disease that can be cured?",
    "Do telomeres really determine our lifespan?",
    "Can rapamycin extend human healthspan?",
    "What causes mitochondrial dysfunction in aging?",
]
