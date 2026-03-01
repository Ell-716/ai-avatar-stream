export interface StreamStatus {
  is_running: boolean;
  current_turn: number;
  current_topic: string;
  max_turns: number;
  errors: string[];
}

export interface Agent {
  name: string;
  voice_id: string;
  color: string;
  system_prompt: string;
  avatar_idle: string;
  avatar_talk_small: string;
  avatar_talk_medium: string;
}

export interface TranscriptMessage {
  timestamp: string;
  agent_name: string;
  text: string;
  topic?: string;
}

export interface WebSocketMessage {
  type: 'connection' | 'transcript' | 'topic_change' | 'status';
  message?: string;
  data?: TranscriptMessage | StreamStatus;
}

export interface ConfigUpdate {
  max_turns: number;
  pause_between_turns: number;
}

export interface LogEntry {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
}
