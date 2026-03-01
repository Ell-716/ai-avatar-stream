import { useState, useEffect } from 'react';
import { StreamControls } from './components/StreamControls';
import { TranscriptViewer } from './components/TranscriptViewer';
import { ConfigPanel } from './components/ConfigPanel';
import { LogsViewer } from './components/LogsViewer';
import { streamAPI, createWebSocket } from './api/client';
import type { StreamStatus, TranscriptMessage } from './types';

function App() {
  const [status, setStatus] = useState<StreamStatus | null>(null);
  const [transcriptMessages, setTranscriptMessages] = useState<TranscriptMessage[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [maxTurns, setMaxTurns] = useState(5);
  const [pauseBetweenTurns, setPauseBetweenTurns] = useState(1);

  // Fetch initial status once on mount
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await streamAPI.getStatus();
        setStatus(response.data);
      } catch (error) {
        console.error('Failed to fetch initial status:', error);
      }
    };

    fetchStatus();
  }, []);

  // Setup WebSocket for real-time transcript and status updates
  useEffect(() => {
    const websocket = createWebSocket((data) => {
      if (data.type === 'transcript' && data.data) {
        setTranscriptMessages((prev) => [...prev, data.data]);
        addLog('info', `${data.data.agent_name} spoke`);
      }
      if (data.type === 'status' && data.data) {
        setStatus(data.data);
      }
      if (data.type === 'connection') {
        addLog('info', 'Connected to transcript stream');
      }
    });

    return () => {
      websocket.close();
    };
  }, []);

  const addLog = (level: string, message: string) => {
    setLogs((prev) => [
      ...prev,
      { timestamp: new Date().toISOString(), level, message },
    ]);
  };

  const handleStart = async () => {
    setIsLoading(true);
    try {
      await streamAPI.start(maxTurns);
      addLog('info', `Stream started with ${maxTurns} turns`);
      setTranscriptMessages([]); // Clear previous transcript
    } catch (error: any) {
      addLog('error', error.response?.data?.detail || 'Failed to start stream');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = async () => {
    setIsLoading(true);
    try {
      await streamAPI.stop();
      addLog('info', 'Stream stopped');
    } catch (error: any) {
      addLog('error', error.response?.data?.detail || 'Failed to stop stream');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveConfig = async (config: any) => {
    try {
      // Update local state with config values
      if (config.max_turns !== undefined) {
        setMaxTurns(config.max_turns);
      }
      if (config.pause_between_turns !== undefined) {
        setPauseBetweenTurns(config.pause_between_turns);
      }

      // For MVP, just log - full implementation would call configAPI.updateConfig
      addLog('info', 'Config updated (restart stream to apply)');
    } catch (error) {
      addLog('error', 'Failed to save config');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
            AI Avatar Stream
          </h1>
          <p className="text-gray-400">Control Panel</p>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            <StreamControls
              status={status}
              onStart={handleStart}
              onStop={handleStop}
              isLoading={isLoading}
            />
            <ConfigPanel
              onSave={handleSaveConfig}
              disabled={status?.is_running || false}
              initialMaxTurns={maxTurns}
              initialPause={pauseBetweenTurns}
            />
          </div>

          {/* Middle Column */}
          <div className="lg:col-span-2">
            <TranscriptViewer messages={transcriptMessages} />
          </div>
        </div>

        {/* Bottom Row */}
        <div className="mt-6">
          <LogsViewer logs={logs} />
        </div>
      </div>
    </div>
  );
}

export default App;
