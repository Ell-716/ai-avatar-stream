import { useState, useEffect } from 'react';
import { Settings } from 'lucide-react';

interface Props {
  onSave: (config: any) => void;
  disabled: boolean;
  initialMaxTurns: number;
  initialPause: number;
}

export function ConfigPanel({ onSave, disabled, initialMaxTurns, initialPause }: Props) {
  const [maxTurns, setMaxTurns] = useState(initialMaxTurns);
  const [pause, setPause] = useState(initialPause);

  // Update local state when props change
  useEffect(() => {
    setMaxTurns(initialMaxTurns);
  }, [initialMaxTurns]);

  useEffect(() => {
    setPause(initialPause);
  }, [initialPause]);

  const handleSave = () => {
    onSave({
      max_turns: maxTurns,
      pause_between_turns: pause,
    });
  };

  return (
    <div className="bg-gray-800/50 backdrop-blur rounded-lg p-6 border border-gray-700">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-5 h-5" />
        <h2 className="text-xl font-bold">Configuration</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Max Turns
          </label>
          <input
            type="number"
            value={maxTurns}
            onChange={(e) => setMaxTurns(parseInt(e.target.value))}
            disabled={disabled}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white disabled:opacity-50"
            min="1"
            max="20"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Pause Between Turns (seconds)
          </label>
          <input
            type="number"
            value={pause}
            onChange={(e) => setPause(parseInt(e.target.value))}
            disabled={disabled}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white disabled:opacity-50"
            min="1"
            max="10"
          />
        </div>

        <button
          onClick={handleSave}
          disabled={disabled}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Save Config
        </button>

        {disabled && (
          <p className="text-xs text-yellow-500">
            Stop the stream to change configuration
          </p>
        )}
      </div>
    </div>
  );
}
