from config import DIALOGUE_HTML

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>AI Discussion — Live</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: transparent;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 28px 32px;
    font-family: 'IBM Plex Mono', monospace;
  }

  .card {
    background: rgba(10, 10, 14, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px 24px 22px;
    max-width: 820px;
    width: 100%;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
  }

  .waiting {
    color: rgba(255, 255, 255, 0.6);
    font-size: 16px;
    text-align: center;
    padding: 30px;
  }
</style>
</head>
<body>
<div class="card">
  <div class="waiting">⏳ Starting AI Discussion...</div>
</div>
</body>
</html>"""

with open(DIALOGUE_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Overlay reset to default state")