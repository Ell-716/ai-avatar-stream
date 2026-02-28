# AI Avatar Discussion Stream

Two AI agents debate longevity and aging biology — live on YouTube.

---

## Project Structure

```
ai-avatar-stream/
│
├── main.py             
├── config.py            
├── dialogue.py          
├── tts.py              
├── overlay.py          
├── transcript.py       
│
├── dialogue.html        
│
├── .env.example         
├── .env                 
├── requirements.txt     
├── README.md           
│
├── audio/              
│   ├── opening.mp3
│   ├── turn_0.mp3
│   ├── turn_1.mp3
│   └── ...
│
└── avatars/            
    ├── agent1.png          
    ├── agent1_talking.png   
    ├── agent2.png           
    └── agent2_talking.png   
```

---

## 1. Install

```bash
pip install -r requirements.txt
```

## 2. API Keys

Copy `.env.example` to `.env`, then fill in your keys:

```bash
cp .env.example .env
```

Open `.env` in any text editor:
- GROQ_API_KEY  →  from https://console.groq.com/
- ELEVENLABS_API_KEY  →  from https://elevenlabs.io/

Voice IDs are pre-filled with defaults. If you want different voices,
browse them at https://elevenlabs.io/docs/guides/voices and update
VOICE_ID_ELENA / VOICE_ID_MARCUS in `.env`.

## 3. Add Avatars

Put 6 images into the `avatars/` folder:

| File                    | What it is                                  |
|-------------------------|---------------------------------------------|
| agent1.png              | Dr. Elena — idle (mouth closed)             | 
| agent1_talk_small.png   | Dr. Elena — talks small (mouth open)        |
| agent1_talk_medium.png  | Dr. Elena - talks medium (mouth more open)  |
| agent2.png              | Prof. Marcus — idle                         |
| agent2_talk_small.png   | Prof. Marcus — talks small                  |
| agent2_talk_medium.png  | Prof. Marcus - talk medium                  |

## 4. Run Locally (test before streaming)

```bash
python main.py
```

You'll see dialogue in the terminal and hear it out loud.
Open `dialogue.html` in a browser to preview the overlay.

## 5. Set Up OBS for Streaming

1. Download OBS Studio: https://obsproject.com/
2. Create a new Scene called "AI Discussion"
3. Add sources (bottom-to-top order in OBS = back-to-front on screen):

   a) **Color Source** — solid black background  
   b) **Image** → avatars/agent1.png — position left  
   c) **Image** → avatars/agent2.png — position right  
   d) **Browser Source** → check "Local file" → point to dialogue.html  
      Width: 1000, Height: 250, position at bottom center  
   e) **Audio Output Capture** — captures your system audio (the TTS)  

4. Video settings: 1280×720, 30 fps

## 6. Go Live on YouTube

1. YouTube Studio → Go Live → Stream (not "Camera" — the "Stream" tab)
2. Copy the Stream Key
3. OBS → Settings → Output → Stream:
   - Service: YouTube
   - Stream Key: paste here
4. Click "Start Streaming" in OBS
5. Run `python main.py`
6. Watch it go!

---

## Tweaking Things

| What                          | Where to change                |
|-------------------------------|--------------------------------|
| Agent names / personalities   | config.py → AGENTS             |
| Discussion topics             | config.py → TOPICS             |
| How long the stream runs      | config.py → MAX_TURNS          |
| Pause between speakers        | config.py → PAUSE_BETWEEN_TURNS|
| Agent colors in overlay       | config.py → AGENTS[x]["color"] |
| Voices                        | .env → VOICE_ID_ELENA / MARCUS |
