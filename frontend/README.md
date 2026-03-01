# AI Avatar Stream - Frontend

React dashboard for controlling the AI discussion stream.

## Development

```bash
npm install
npm run dev
```

Open http://localhost:5173

## Environment Variables

Create `.env`:

**For local development (without Docker):**
```env
VITE_API_URL=http://localhost:8000
```

**For Docker deployment (with Nginx proxy):**
```env
VITE_API_URL=
```

Leave `VITE_API_URL` empty when using Docker Compose. Nginx will proxy `/api` and `/ws` requests to the backend container.

## Features

- 🎮 Start/Stop stream controls
- 📝 Live transcript viewer (WebSocket)
- ⚙️ Configuration panel
- 📊 Real-time status updates
- 🐛 Logs and error viewer

## Tech Stack

- React 18 + TypeScript
- Vite
- Tailwind CSS
- Axios + React Query
- WebSocket
