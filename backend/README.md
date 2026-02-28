# FastAPI Backend - AI Avatar Stream

REST API and WebSocket interface for controlling the AI avatar discussion stream programmatically.

## Overview

This backend provides:
- **REST API** for stream control and configuration
- **WebSocket** for real-time transcript updates
- **Swagger UI** for interactive API documentation
- **Thread-safe stream management** ensuring only one stream runs at a time

## Running the Server

### Method 1: Using uvicorn directly

```bash
# From project root
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Using Python module

```bash
# From project root
python -m backend.main
```

### Method 3: Using the startup script

```bash
# From project root
python3 backend/main.py
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation with Swagger UI.

## Endpoints

### Health Check

- `GET /health` - Health check endpoint

### Stream Control

- `POST /api/stream/start` - Start the AI discussion stream
  - **Body**: `{"max_turns": 5}` (optional, default: 5)
  - **Returns**: Stream status
  - **Status Codes**:
    - 200: Success
    - 409: Stream already running

- `POST /api/stream/stop` - Stop the running stream
  - **Returns**: Success message
  - **Status Codes**:
    - 200: Success
    - 400: No stream running

- `GET /api/stream/status` - Get current stream status
  - **Returns**:
    - `is_running`: Boolean
    - `current_turn`: Integer
    - `current_topic`: String
    - `max_turns`: Integer
    - `errors`: Array of recent error messages

### Configuration

- `GET /api/config/agents` - Get all agent configurations
  - **Returns**: Dictionary of agent configs with voice IDs, colors, system prompts

- `GET /api/config/topics` - Get available discussion topics
  - **Returns**: Array of topic strings

- `GET /api/config/settings` - Get all stream settings
  - **Returns**: Current configuration values

- `PUT /api/config` - Update stream configuration
  - **Body**:
    ```json
    {
      "max_turns": 10,
      "pause_between_turns": 2.0,
      "topics": ["New topic 1", "New topic 2"]
    }
    ```
  - **Note**: Updates apply to next stream run, not current

### WebSocket

- `WS /ws/transcript` - Real-time transcript updates

  **Message Format (Server → Client)**:
  ```json
  {
    "timestamp": "2026-02-28T14:32:15.123456",
    "agent_name": "Dr. Elena",
    "text": "That's a fascinating point...",
    "topic": "What is consciousness?",
    "turn": 5
  }
  ```

  **Client Commands**:
  ```json
  {"command": "ping"}        // Responds with {"type": "pong"}
  {"command": "status"}      // Responds with current stream status
  ```

## Testing

### Using curl

```bash
# Start stream
curl -X POST http://localhost:8000/api/stream/start \
  -H "Content-Type: application/json" \
  -d '{"max_turns": 3}'

# Check status
curl http://localhost:8000/api/stream/status

# Stop stream
curl -X POST http://localhost:8000/api/stream/stop

# Get agents
curl http://localhost:8000/api/config/agents

# Get topics
curl http://localhost:8000/api/config/topics

# Update config
curl -X PUT http://localhost:8000/api/config \
  -H "Content-Type: application/json" \
  -d '{"max_turns": 10, "pause_between_turns": 2.5}'
```

### Using httpie

```bash
# Start stream
http POST localhost:8000/api/stream/start max_turns:=3

# Check status
http GET localhost:8000/api/stream/status

# Stop stream
http POST localhost:8000/api/stream/stop
```

### Testing WebSocket

Install wscat:
```bash
npm install -g wscat
```

Connect to transcript WebSocket:
```bash
wscat -c ws://localhost:8000/ws/transcript
```

You'll receive real-time transcript messages as the stream runs.

Send commands:
```bash
# Ping
> {"command": "ping"}

# Get status
> {"command": "status"}
```

### Using Python

```python
import requests

# Start stream
response = requests.post(
    "http://localhost:8000/api/stream/start",
    json={"max_turns": 5}
)
print(response.json())

# Get status
status = requests.get("http://localhost:8000/api/stream/status")
print(status.json())

# Stop stream
requests.post("http://localhost:8000/api/stream/stop")
```

WebSocket client:
```python
import asyncio
import websockets
import json

async def listen_transcript():
    uri = "ws://localhost:8000/ws/transcript"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"[{data['agent_name']}]: {data['text']}")

asyncio.run(listen_transcript())
```

## Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── routers/
│   ├── stream.py          # Stream control endpoints
│   └── config.py          # Configuration endpoints
├── services/
│   └── stream_manager.py  # Singleton stream lifecycle manager
├── websockets/
│   └── transcript.py      # Real-time transcript WebSocket
└── models/
    └── schemas.py         # Pydantic request/response models
```

### StreamManager Service

The `StreamManager` is a singleton service that:
- Ensures only one stream runs at a time
- Manages stream state (running/stopped)
- Runs streams in background threads
- Broadcasts transcript updates to WebSocket clients
- Provides thread-safe operations

## CORS Configuration

The API includes CORS middleware to allow requests from:
- http://localhost:3000 (Create React App)
- http://localhost:5173 (Vite)
- http://localhost:5174 (Alternative Vite port)

Additional origins can be configured in `backend/main.py`.

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Successful operation
- **400 Bad Request**: Invalid request (e.g., stopping when not running)
- **409 Conflict**: Resource conflict (e.g., starting when already running)
- **500 Internal Server Error**: Unexpected server error

All errors return JSON with a `detail` field:
```json
{
  "detail": "Error message here"
}
```

## Logging

All API requests and stream events are logged using the centralized logger.

Logs are written to:
- **Console**: Colored output for development
- **File**: `logs/app.log` with rotation

## Integration with Frontend

The backend is designed to work with a React frontend. Example frontend code:

```javascript
// Start stream
const startStream = async (maxTurns = 5) => {
  const response = await fetch('http://localhost:8000/api/stream/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ max_turns: maxTurns })
  });
  return response.json();
};

// WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/transcript');
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(`[${message.agent_name}]: ${message.text}`);
};
```

## Standalone Script Compatibility

The original standalone script (`main.py` in project root) continues to work unchanged:

```bash
python3 main.py
```

The backend and standalone script share the same core logic in the `core/` directory.
