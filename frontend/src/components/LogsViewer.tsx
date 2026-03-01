import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';

interface LogEntry {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
}

interface Props {
  logs: LogEntry[];
}

export function LogsViewer({ logs }: Props) {
  const getIcon = (level: string) => {
    switch (level) {
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      default:
        return <CheckCircle className="w-4 h-4 text-green-500" />;
    }
  };

  return (
    <div className="bg-gray-800/50 backdrop-blur rounded-lg p-6 border border-gray-700">
      <h2 className="text-xl font-bold mb-4">Logs & Errors</h2>

      <div className="h-48 overflow-y-auto space-y-2">
        {logs.length === 0 ? (
          <div className="text-gray-500 text-sm text-center py-4">
            No logs yet
          </div>
        ) : (
          logs.map((log, idx) => (
            <div key={idx} className="flex items-start gap-2 text-sm">
              {getIcon(log.level)}
              <span className="text-gray-400 text-xs">
                {new Date(log.timestamp).toLocaleTimeString()}
              </span>
              <span className="text-gray-200 flex-1">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
