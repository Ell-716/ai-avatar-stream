# AI Avatar Discussion Stream

Two autonomous AI agents with animated avatars discuss longevity and aging biology in real-time on YouTube. No human intervention required.

**🎥 [Watch Live Demo on YouTube](https://youtube.com/live/MfnclZWCSUk)**

---

## Features

✅ **Autonomous AI Dialogue** — Groq LLM generates natural conversation between two distinct personalities  
✅ **Text-to-Speech** — ElevenLabs voices with different tones for each agent  
✅ **Lip-Sync Animation** — Mouth movements synchronized with speech  
✅ **Real-Time Overlay** — Dynamic dialogue subtitles update during the stream  
✅ **Live Streaming** — Direct integration with YouTube via OBS WebSocket  
✅ **Transcript Logging** — Full conversation saved with timestamps

---

## Tech Stack

- **LLM**: Groq API (Llama 3.3 70B Versatile)
- **TTS**: ElevenLabs API
- **Streaming**: OBS Studio + WebSocket automation
- **Orchestration**: Python
- **Avatars**: AI-generated portraits (Artlist Nano Banana Pro)

---

## Project Structure

```
ai-avatar-stream/
│
├── main.py                  # Entry point — orchestrates the entire flow
├── config.py                # All settings (agents, topics, timing)
├── dialogue.py              # Groq LLM conversation logic
├── tts.py                   # ElevenLabs speech generation + playback
├── avatar.py                # OBS WebSocket control for avatar swapping
├── overlay.py               # Rewrites dialogue.html for OBS browser source
├── transcript.py            # Logs conversation with timestamps
├── reset_overlay.py         # Resets dialogue display before streaming
│
├── dialogue.html            # OBS browser source overlay (auto-updated)
├── requirements.txt         # Python dependencies
├── .env.example             # API key template
│
├── audio/                   # Generated TTS files (created at runtime)
│   ├── opening.mp3
│   ├── turn_0.mp3
│   └── ...
│
└── avatars/                 # AI-generated avatar portraits
    ├── agent1.png
    ├── agent1_talk_small.png
    ├── agent1_talk_medium.png
    ├── agent2.png
    ├── agent2_talk_small.png
    └── agent2_talk_medium.png
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
- `GROQ_API_KEY` → Get from [console.groq.com](https://console.groq.com/)
- `ELEVENLABS_API_KEY` → Get from [elevenlabs.io](https://elevenlabs.io/)

Optional: Customize voice IDs for each agent in `.env`

### 3. Test Locally

```bash
python main.py
```

You'll hear the agents talking and see dialogue in the terminal. Check `transcript.txt` for the full conversation log.

### 4. Stream to YouTube (Optional)

**Prerequisites:**
- OBS Studio installed
- YouTube live streaming enabled (24h activation period for new channels)

**OBS Setup:**

1. Create scene "AI Discussion"
2. Add sources (order matters):
   - **Color Source** → black background
   - **Image** → `avatars/agent1.png` (right side)
   - **Image** → `avatars/agent2.png` (left side)
   - **Browser Source** → Local file: `dialogue.html` (1000×250px, bottom center)
   - **macOS Audio Capture** → captures TTS audio
3. Settings → Video → 1280×720, 30fps
4. Settings → Stream → Connect to YouTube

**Go Live:**

```bash
python reset_overlay.py    # Clear old dialogue
```

Start Streaming in OBS, wait 10 seconds, then:

```bash
python main.py
```

---

## Configuration

All settings are in `config.py`:

| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_TURNS` | Number of back-and-forth exchanges | 5 |
| `PAUSE_BETWEEN_TURNS` | Silence between speakers (seconds) | 1 |
| `TOPICS` | Discussion topics pool | 8 aging biology topics |
| `AGENTS` | Agent personalities, voices, colors | Dr. Elena (optimist), Prof. Marcus (skeptic) |

---

## How It Works

1. **Dialogue Generation**: Groq LLM generates contextual responses based on agent personalities and conversation history
2. **Speech Synthesis**: ElevenLabs converts text to speech with distinct voices
3. **Avatar Animation**: Python controls OBS via WebSocket to swap avatar images (idle ↔ talking states)
4. **Overlay Update**: `dialogue.html` is rewritten each turn, OBS browser source auto-refreshes
5. **Audio Playback**: TTS plays through system audio, OBS captures it for the stream
6. **Logging**: Every message saved to `transcript.txt` with timestamps

---

## Agents

**Dr. Elena** (Agent 1)  
*Optimistic molecular biologist*  
Believes aging can be reversed with the right interventions. References recent research enthusiastically.

**Prof. Marcus** (Agent 2)  
*Skeptical gerontologist*  
Demands rigorous evidence. Points out flaws in reasoning respectfully.

Both agents keep responses to 1-2 sentences for natural pacing.

---

## Demo

**Live Stream:** [https://youtube.com/live/MfnclZWCSUk](https://youtube.com/live/MfnclZWCSUk)

The stream demonstrates:
- Autonomous conversation (no human input during recording)
- Real-time dialogue updates
- Synchronized avatar mouth animation
- Natural topic transitions

---

## Notes

- **Lip-sync**: Uses static image swapping (idle/small/medium mouth states) rather than true video lip-sync
- **Avatar quality**: Photorealistic AI-generated portraits with natural skin texture
- **Context window**: Agents remember the last 6 messages for conversational coherence
- **Topic switching**: Automatically changes topics every 8 turns

---

## License

MIT