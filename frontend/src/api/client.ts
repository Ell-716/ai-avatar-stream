import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Stream endpoints
export const streamAPI = {
  start: (maxTurns: number = 5) =>
    api.post('/api/stream/start', { max_turns: maxTurns }),

  stop: () =>
    api.post('/api/stream/stop', {}),

  getStatus: () =>
    api.get('/api/stream/status'),
};

// Config endpoints
export const configAPI = {
  getAgents: () =>
    api.get('/api/config/agents'),

  getTopics: () =>
    api.get('/api/config/topics'),

  updateConfig: (config: any) =>
    api.put('/api/config', config),
};

// WebSocket helper
export const createWebSocket = (onMessage: (data: any) => void) => {
  // Determine WebSocket URL based on environment
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsHost = API_BASE_URL
    ? API_BASE_URL.replace(/^https?:/, wsProtocol)
    : `${wsProtocol}//${window.location.host}`;
  const wsUrl = `${wsHost}/ws/transcript`;

  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('WebSocket connected');
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  ws.onclose = () => {
    console.log('WebSocket disconnected');
  };

  return ws;
};
