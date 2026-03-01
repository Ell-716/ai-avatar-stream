import { Play, Square, Loader2 } from 'lucide-react';
import type { StreamStatus } from '../types';

interface Props {
  status: StreamStatus | null;
  onStart: () => void;
  onStop: () => void;
  isLoading: boolean;
}

export function StreamControls({ status, onStart, onStop, isLoading }: Props) {
  return (
    <div className="bg-gray-800/50 backdrop-blur rounded-lg p-6 border border-gray-700">
      <h2 className="text-xl font-bold mb-4">Stream Control</h2>

      <div className="space-y-4">
        {/* Status indicator */}
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${status?.is_running ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
          <span className="text-sm font-medium">
            {status?.is_running ? 'LIVE' : 'STOPPED'}
          </span>
        </div>

        {/* Turn progress */}
        {status?.is_running && (
          <div>
            <div className="text-sm text-gray-400 mb-1">Progress</div>
            <div className="text-lg font-mono">
              Turn {status.current_turn}/{status.max_turns}
            </div>
          </div>
        )}

        {/* Current topic */}
        {status?.current_topic && (
          <div>
            <div className="text-sm text-gray-400 mb-1">Topic</div>
            <div className="text-sm">{status.current_topic}</div>
          </div>
        )}

        {/* Control buttons */}
        <div className="flex gap-2 pt-2">
          {!status?.is_running ? (
            <button
              onClick={onStart}
              disabled={isLoading}
              className="flex items-center gap-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-medium transition-colors"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Play className="w-4 h-4" />
              )}
              Start Stream
            </button>
          ) : (
            <button
              onClick={onStop}
              disabled={isLoading}
              className="flex items-center gap-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-medium transition-colors"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Square className="w-4 h-4" />
              )}
              Stop Stream
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
