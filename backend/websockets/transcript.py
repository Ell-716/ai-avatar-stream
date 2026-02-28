"""
WebSocket endpoint for real-time transcript updates.

Provides a WebSocket connection that streams transcript messages
as they are generated during the AI discussion.

Uses a thread-safe queue to receive messages from the sync stream thread.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.stream_manager import StreamManager
from logger import get_logger
import asyncio
import json

logger = get_logger(__name__)
router = APIRouter()

# Get singleton instance
stream_manager = StreamManager()


@router.websocket("/ws/transcript")
async def transcript_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time transcript updates.

    Clients connect to this endpoint and receive transcript messages
    as agents speak during the discussion.

    Message format:
    {
        "timestamp": "2026-02-28T14:32:15.123456",
        "agent_name": "Dr. Elena",
        "text": "That's a fascinating point...",
        "topic": "What is consciousness?",
        "turn": 5
    }

    For topic changes, agent_name will be empty and topic will be set.
    """
    await websocket.accept()
    logger.info("WebSocket client connected")

    # Send welcome message
    try:
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to transcript stream",
            "status": stream_manager.get_status()
        })
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")
        return

    # Flag to stop background tasks
    stop_tasks = asyncio.Event()

    async def send_transcript_messages():
        """
        Background task to poll the queue and send transcript messages.
        Runs until WebSocket disconnects or stop_tasks is set.
        """
        try:
            while not stop_tasks.is_set():
                # Check if there are messages in the queue (non-blocking)
                if not stream_manager.transcript_queue.empty():
                    try:
                        message = stream_manager.transcript_queue.get_nowait()
                        await websocket.send_json(message)
                        logger.debug(f"Sent transcript message: {message.get('agent_name', 'topic_change')}")
                    except Exception as e:
                        logger.error(f"Error sending transcript message: {e}")
                        break

                # Sleep briefly to avoid busy-waiting
                await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            logger.debug("Transcript sender task cancelled")
        except Exception as e:
            logger.error(f"Error in transcript sender: {e}")

    async def receive_client_messages():
        """
        Background task to receive and process client messages.
        Runs until WebSocket disconnects or stop_tasks is set.
        """
        try:
            while not stop_tasks.is_set():
                # Receive message from client with timeout
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                except asyncio.TimeoutError:
                    # No message received, continue loop
                    continue

                # Parse and handle client message
                try:
                    client_message = json.loads(data)
                    command = client_message.get("command")

                    if command == "ping":
                        await websocket.send_json({"type": "pong"})
                    elif command == "status":
                        status = stream_manager.get_status()
                        await websocket.send_json({
                            "type": "status",
                            "data": status
                        })
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Unknown command: {command}"
                        })

                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client: {data}")
                except Exception as e:
                    logger.error(f"Error processing client message: {e}")

        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
            stop_tasks.set()
        except asyncio.CancelledError:
            logger.debug("Client message receiver task cancelled")
        except Exception as e:
            logger.error(f"Error in client message receiver: {e}")
            stop_tasks.set()

    # Run both tasks concurrently
    sender_task = asyncio.create_task(send_transcript_messages())
    receiver_task = asyncio.create_task(receive_client_messages())

    try:
        # Wait for either task to complete (usually due to disconnect)
        done, pending = await asyncio.wait(
            [sender_task, receiver_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel any remaining tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        stop_tasks.set()
        logger.info("WebSocket connection closed")
