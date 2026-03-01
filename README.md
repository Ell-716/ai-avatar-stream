# AI Avatar Discussion Stream

Autonomous AI agents with animated avatars discuss longevity science live on YouTube. Two AI personalities engage in real-time scientific debates with voice synthesis, lip-sync animation, and automated streaming—all without human intervention.

**🎥 [Watch Live Demo on YouTube](https://youtube.com/live/MfnclZWCSUk)**

---

## ✨ Features

- 🤖 **Autonomous AI Dialogue** — Groq LLM (Llama 3.3 70B) generates natural conversation between distinct personalities
- 🎙️ **Voice Synthesis** — ElevenLabs TTS with unique voices for each agent
- 👄 **Lip-Sync Animation** — Mouth movements synchronized with speech using image swapping
- 📺 **Live Streaming** — Direct YouTube integration via OBS Studio
- 🌐 **Web Control Panel** — React dashboard to start/stop streams and monitor in real-time
- 📝 **Live Transcript** — WebSocket-powered real-time conversation viewer
- 💾 **Logging** — Production-grade error handling and transcript archiving
- 🐳 **Docker Ready** — Containerized deployment with docker-compose
- 🔄 **CI/CD Pipeline** — Automated testing and linting via GitHub Actions

---

## 🏗️ Tech Stack

**Backend:**
- FastAPI (Python) — REST API + WebSocket server
- Groq API — LLM dialogue generation (Llama 3.3 70B Versatile)
- ElevenLabs API — Text-to-speech synthesis
- OBS WebSocket — Real-time scene control

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS
- Axios + WebSocket client

**Infrastructure:**
- Docker + Docker Compose
- Nginx (production reverse proxy)
- GitHub Actions (CI/CD)

**Code Quality:**
- Python: Ruff, Black, isort
- TypeScript: ESLint, TypeScript compiler

---

## 📁 Project Structure

```
ai-avatar-stream/
├── backend/                    # FastAPI REST API
│   ├── main.py                 # API server entry point
│   ├── routers/                # API endpoints
│   │   ├── stream.py           # Stream control endpoints
│   │   └── config.py           # Configuration endpoints
│   ├── services/               # Business logic
│   │   └── stream_manager.py   # Stream orchestration
│   ├── websockets/             # Real-time communication
│   │   └── transcript.py       # WebSocket transcript handler
│   └── models/                 # Pydantic schemas
│       └── schemas.py          # API request/response models
│
├── frontend/                   # React control panel
│   ├── src/
│   │   ├── components/         # UI components
│   │   │   ├── StreamControls.tsx    # Start/stop buttons
│   │   │   ├── TranscriptViewer.tsx  # Live transcript display
│   │   │   ├── ConfigPanel.tsx       # Settings panel
│   │   │   └── LogsViewer.tsx        # Log viewer
│   │   ├── api/                # API client
│   │   │   └── client.ts       # Axios HTTP client
│   │   └── types/              # TypeScript definitions
│   │       └── index.ts        # Type declarations
│   ├── public/                 # Static assets
│   ├── package.json            # Node dependencies
│   ├── vite.config.ts          # Vite configuration
│   ├── tsconfig.json           # TypeScript config
│   ├── tailwind.config.js      # Tailwind CSS config
│   └── eslint.config.js        # ESLint rules
│
├── core/                       # AI stream logic
│   ├── dialogue.py             # Groq LLM integration
│   ├── tts.py                  # ElevenLabs TTS
│   ├── avatar.py               # OBS WebSocket control
│   ├── overlay.py              # Dialogue HTML generation
│   └── transcript.py           # Logging utilities
│
├── avatars/                    # AI-generated portraits
│   ├── agent1.png              # Dr. Elena (idle)
│   ├── agent1_talk_small.png   # Slight mouth opening
│   ├── agent1_talk_medium.png  # Medium mouth opening
│   ├── agent2.png              # Prof. Marcus (idle)
│   ├── agent2_talk_small.png   # Slight mouth opening
│   └── agent2_talk_medium.png  # Medium mouth opening
│
├── audio/                      # Generated TTS audio files
│   ├── opening.mp3             # Opening message
│   └── turn_*.mp3              # Per-turn audio clips
│
├── logs/                       # Application logs
│   └── app.log                 # Runtime logs and errors
│
├── utils/                      # Shared utilities
│   └── retry.py                # Retry decorator for API calls
│
├── .github/workflows/          # CI/CD automation
│   └── ci.yml                  # GitHub Actions pipeline
│
├── main.py                     # Standalone CLI script
├── config.py                   # Configuration settings
├── logger.py                   # Centralized logging setup
├── dialogue.html               # OBS browser source overlay
├── transcript.txt              # Saved conversation history
├── reset_overlay.py            # Clear dialogue overlay
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── docker-compose.yml          # Container orchestration
├── Dockerfile.backend          # Backend image
├── Dockerfile.frontend         # Frontend image (multi-stage)
├── nginx.conf                  # Production reverse proxy config
├── .dockerignore               # Docker build exclusions
├── .isort.cfg                  # Import sorting config
├── .ruff.toml                  # Python linter config
└── DEPLOYMENT.md               # Detailed deployment guide
```

---

## 🚀 Quick Start

### Method 1: Docker (Recommended)

**Prerequisites:** Docker, Docker Compose

```bash
# 1. Clone repository
git clone https://github.com/Ell-716/ai-avatar-stream.git
cd ai-avatar-stream

# 2. Configure API keys
cp .env.example .env
# Edit .env and add your GROQ_API_KEY and ELEVENLABS_API_KEY

# 3. Start services
docker-compose up --build

# 4. Access the application
# - Frontend: http://localhost
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

**What you get:**
- ✅ Full-stack app running in containers
- ✅ Web control panel to start/stop streams
- ✅ Live transcript viewer
- ✅ API for programmatic control
- ❌ No audio playback (Docker limitation)
- ❌ No OBS integration (use Method 2 for YouTube streaming)

---

### Method 2: Local Development (For YouTube Streaming)

**Prerequisites:** Python 3.12+, Node.js 20+, OBS Studio

#### Backend Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start backend
uvicorn backend.main:app --reload
# Backend API: http://localhost:8000
```

#### Frontend Setup (Optional)

```bash
# 1. Install Node dependencies
cd frontend
npm install

# 2. Start dev server
npm run dev
# Frontend: http://localhost:5173
```

#### OBS Configuration

1. **Download OBS Studio**: https://obsproject.com/
2. **Enable WebSocket**: Tools → WebSocket Server Settings → Enable (port 4455)
3. **Create Scene** "AI Discussion" with sources (bottom → top):
   - **Color Source** → Black background (#000000)
   - **Image** → `avatars/agent2.png` (position left)
   - **Image** → `avatars/agent1.png` (position right)
   - **Browser Source** → Local file: `dialogue.html`, 1000×250px, bottom center
   - **macOS Audio Capture** → Captures TTS audio
4. **Video Settings**: 1280×720, 30fps
5. **Stream Settings**: YouTube, add Stream Key

#### Run the Stream

```bash
# Option A: Via frontend (if running)
# Open http://localhost:5173 and click "Start Stream"

# Option B: Standalone script
python reset_overlay.py  # Clear old dialogue
python main.py           # Start AI discussion
```

---

## 🎛️ Configuration

Edit `config.py` to customize:

```python
# Stream settings
MAX_TURNS = 5                   # Number of exchanges
PAUSE_BETWEEN_TURNS = 1         # Seconds between speakers

# Agent personalities
AGENTS = {
    "agent1": {
        "name": "Dr. Elena",
        "voice_id": "...",          # ElevenLabs voice ID
        "color": "#00ff88",         # UI accent color
        "system_prompt": "..."      # LLM personality
    },
    "agent2": { ... }
}

# Discussion topics
TOPICS = [
    "Why do organs age differently?",
    "Are epigenetic clocks accurate?",
    # Add your own topics...
]
```

---

## 📡 API Reference

### REST Endpoints

**Stream Control:**
- `POST /api/stream/start` — Start AI discussion
- `POST /api/stream/stop` — Stop current stream
- `GET /api/stream/status` — Get stream state

**Configuration:**
- `GET /api/config/agents` — Get agent settings
- `GET /api/config/topics` — Get available topics
- `PUT /api/config` — Update configuration

**Health:**
- `GET /health` — Service health check

### WebSocket

**Endpoint:** `ws://localhost:8000/ws/transcript`

**Message Format:**
```json
{
  "type": "transcript",
  "data": {
    "timestamp": "2026-03-01T14:30:00",
    "agent_name": "Dr. Elena",
    "text": "I think telomere research shows...",
    "topic": "Do telomeres determine lifespan?"
  }
}
```

**Full documentation:** http://localhost:8000/docs

---

## 🎭 The Agents

### Dr. Elena
**Role:** Optimistic Molecular Biologist  
**Personality:** Enthusiastic about anti-aging breakthroughs, cites recent research, believes aging is reversible  
**Voice:** Warm, energetic (ElevenLabs voice ID customizable)  
**Color:** `#00ff88` (green)

### Prof. Marcus
**Role:** Skeptical Gerontologist  
**Personality:** Evidence-focused, points out flaws respectfully, demands rigorous studies  
**Voice:** Measured, thoughtful  
**Color:** `#ff6b6b` (red)

Both keep responses to 1-2 sentences for natural conversational flow.

---

## 🎬 How It Works

```
┌─────────────┐
│   User      │  Clicks "Start Stream" in React UI
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  FastAPI Backend                                    │
│  • Receives API call                                │
│  • Starts stream in background thread               │
└──────┬──────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  Stream Manager                                     │
│  1. Picks random topic                              │
│  2. Loop through turns:                             │
│     • Generate response (Groq LLM)                  │
│     • Convert to speech (ElevenLabs)                │
│     • Update overlay HTML                           │
│     • Broadcast via WebSocket                       │
│     • Swap avatar (OBS WebSocket)                   │
│     • Play audio                                    │
│     • Log to transcript                             │
└──────┬──────────────────────────────────────────────┘
       │
       ├──────────────┬─────────────┬─────────────┐
       │              │             │             │
       ▼              ▼             ▼             ▼
┌──────────┐  ┌──────────-┐   ┌──────────┐  ┌──────────┐
│   OBS    │  │ React UI  │   │  Logs    │  │ YouTube  │
│ (avatars)│  │(transcript)│  │  (.txt)  │  │ (stream) │
└──────────┘  └──────────-┘   └──────────┘  └──────────┘
```

---

## 🐳 Docker Deployment

See **[Method 1: Docker](#method-1-docker-recommended)** in Quick Start above.

**Additional commands:**

```bash
# Run in background (production)
docker-compose up -d

# Monitor logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build

# Stop and remove containers
docker-compose down

# Check container status
docker-compose ps
```

---

## 🔧 Development

### Run Locally

See **[Method 2: Local Development](#method-2-local-development-for-youtube-streaming)** in Quick Start above.

### Code Quality Tools

```bash
# Python
ruff check .        # Lint
black .             # Format
isort .             # Sort imports

# TypeScript
cd frontend
npm run lint        # ESLint
npx tsc --noEmit    # Type check
```

### Testing

```bash
# Test Docker build
docker-compose build

# Test API
curl -X POST http://localhost:8000/api/stream/start \
  -H "Content-Type: application/json" \
  -d '{"max_turns": 2}'

# Test WebSocket
wscat -c ws://localhost:8000/ws/transcript
```

---

## 🚦 CI/CD

GitHub Actions runs automatically on every push:

✅ **Lint & Format**
- Python: Ruff, Black, isort
- TypeScript: ESLint, tsc

✅ **Build**
- Backend Docker image
- Frontend Docker image

✅ **Test**
- docker-compose integration test
- Health check validation

**Status:** Check the Actions tab in your repository

---

## 📊 Monitoring

### Logs

**Docker:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Local:**
```bash
tail -f logs/app.log
```

### Metrics

- Stream duration and turn count logged automatically
- Success rate tracked (successful vs. failed turns)
- All errors logged with timestamps and context

---

## 🎥 YouTube Streaming Guide

### Prerequisites

1. YouTube Channel with live streaming enabled (24h activation for new channels)
2. OBS Studio installed and configured
3. Backend + Frontend running locally (see **[Method 2](#method-2-local-development-for-youtube-streaming)**)

### Quick Workflow

1. **Setup**: Follow Method 2 in Quick Start (above) to configure OBS and start backend
2. **Go Live**: 
   - Start OBS streaming → YouTube
   - Click "Start Stream" in React UI (`http://localhost:5173`)
   - OR run `python main.py` for standalone mode
3. **Monitor**: Watch OBS preview, frontend transcript, and YouTube dashboard
4. **Stop**: Click "Stop Stream" in UI or `Ctrl+C` in terminal, then stop OBS

💡 **Tip**: Run `python reset_overlay.py` before starting to clear old dialogue.

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Code Standards:**
- Python code must pass Ruff, Black, isort
- TypeScript must pass ESLint and type checking
- Add tests for new features
- Update documentation

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **Groq** — Fast LLM inference
- **ElevenLabs** — High-quality TTS
- **OBS Studio** — Professional streaming software
- **Artlist Nano Banana Pro** — AI avatar generation

---

## 🎯 Future Improvements

- [ ] True video lip-sync with D-ID/HeyGen
- [ ] YouTube chat integration
- [ ] Multi-agent support (3+ participants)
- [ ] RAG integration for fact-checking
- [ ] Translate topics to other languages
- [ ] Cloud deployment guide (AWS/GCP)
- [ ] Analytics dashboard

---

**⭐ If you find this project useful, please star it on GitHub!**