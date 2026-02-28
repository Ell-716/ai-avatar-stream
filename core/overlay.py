"""
overlay.py — rewrites dialogue.html every turn.

OBS Browser Source watches this file and auto-refreshes,
so the on-stream subtitle updates in real time.
"""

from config import AGENTS, DIALOGUE_HTML
from logger import get_logger

logger = get_logger(__name__)


def update_overlay(agent_key: str, text: str, topic: str):
    """
    Rewrite dialogue.html with the current speaker, text, and topic.
    OBS will pick up the change automatically.
    """
    agent = AGENTS[agent_key]
    color = agent["color"]          # e.g. "#00ff88"
    name  = agent["name"]           # e.g. "Dr. Elena"

    # We rebuild the file from scratch each time so animations re-trigger.
    # This is intentional — OBS re-renders the page on file change,
    # which restarts CSS animations (slideUp, typeIn, pulse).

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>AI Discussion — Live</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@700;800&display=swap');

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: transparent;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 28px 32px;
    font-family: 'IBM Plex Mono', monospace;
  }}

  .card {{
    background: rgba(10, 10, 14, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px 24px 22px;
    max-width: 820px;
    width: 100%;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    animation: slideUp 0.4s cubic-bezier(.22,.61,0,1) both;
  }}

  @keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to   {{ opacity: 1; transform: translateY(0);    }}
  }}

  .top-bar {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
  }}

  .speaker-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: {color};
    box-shadow: 0 0 8px {color};
    animation: pulse 1.4s ease-in-out infinite;
  }}

  @keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50%      {{ opacity: 0.35; }}
  }}

  .speaker-name {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 18px;
    color: {color};
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}

  .live-badge {{
    margin-left: auto;
    background: #e63946;
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 20px;
  }}

  .dialogue-text {{
    color: rgba(255, 255, 255, 0.92);
    font-size: 17px;
    line-height: 1.6;
    animation: typeIn 0.6s ease both;
  }}

  @keyframes typeIn {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to   {{ opacity: 1; transform: translateY(0);   }}
  }}

  .topic-bar {{
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .topic-label {{
    color: rgba(255,255,255,0.3);
    font-size: 11px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
  }}

  .topic-text {{
    color: rgba(255,255,255,0.55);
    font-size: 13px;
  }}
</style>
</head>
<body>
<div class="card">
  <div class="top-bar">
    <div class="speaker-dot"></div>
    <span class="speaker-name">{name}</span>
    <span class="live-badge">● Live</span>
  </div>
  <div class="dialogue-text">{text}</div>
  <div class="topic-bar">
    <span class="topic-label">Topic</span>
    <span class="topic-text">{topic}</span>
  </div>
</div>
</body>
</html>"""

    # Validate HTML content before writing
    if not html or len(html) < 100:
        logger.error("Generated HTML is too short or empty")
        return

    try:
        with open(DIALOGUE_HTML, "w", encoding="utf-8") as f:
            f.write(html)
        logger.debug(f"Overlay updated for {name}")
    except PermissionError as e:
        logger.critical(f"Permission denied writing overlay file {DIALOGUE_HTML}: {e}")
        return
    except OSError as e:
        logger.critical(f"File system error writing overlay file {DIALOGUE_HTML}: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error writing overlay file: {e}")
        return

    # Force OBS browser source to refresh via WebSocket
    try:
        from core.avatar import ws
        if ws is not None:
            from obswebsocket import requests as obs_requests
            # Press the "Refresh cache" button programmatically
            ws.call(obs_requests.PressInputPropertiesButton(
                inputName="Dialogue",
                propertyName="refreshnocache"
            ))
            logger.debug("OBS browser source refreshed")
    except Exception as e:
        # Fail silently if OBS not connected or command fails
        logger.debug(f"Could not refresh OBS browser source: {e}")
