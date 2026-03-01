import { useEffect, useRef } from 'react';
import type { TranscriptMessage } from '../types';
import { MessageSquare } from 'lucide-react';

interface Props {
  messages: TranscriptMessage[];
}

export function TranscriptViewer({ messages }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="bg-gray-800/50 backdrop-blur rounded-lg p-6 border border-gray-700">
      <div className="flex items-center gap-2 mb-4">
        <MessageSquare className="w-5 h-5" />
        <h2 className="text-xl font-bold">Live Transcript</h2>
      </div>

      <div className="h-96 overflow-y-auto space-y-3 pr-2">
        {messages.length === 0 ? (
          <div className="text-gray-500 text-sm text-center py-8">
            No messages yet. Start a stream to see the conversation.
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="border-l-2 border-gray-700 pl-3">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-gray-400">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </span>
                <span
                  className="text-sm font-semibold"
                  style={{
                    color: msg.agent_name.includes('Elena') ? '#00ff88' : '#ff6b6b'
                  }}
                >
                  {msg.agent_name}
                </span>
              </div>
              <p className="text-sm text-gray-200">{msg.text}</p>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
