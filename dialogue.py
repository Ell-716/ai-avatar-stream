from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_WINDOW, AGENTS

client = Groq(api_key=GROQ_API_KEY)

# Stores the full conversation so agents remember what was said
conversation_history: list[dict] = []


def generate_response(agent_key: str, topic: str) -> str:
    """
    Generate a response from the given agent using Groq.
    Maintains conversation context so the agent knows what was said before.
    """
    agent = AGENTS[agent_key]

    # System prompt defines the agent's personality
    messages = [
        {"role": "system", "content": agent["system_prompt"]},
    ]

    # Add recent conversation history so the agent has context
    # We slice to CONTEXT_WINDOW to avoid hitting token limits
    for entry in conversation_history[-CONTEXT_WINDOW:]:
        messages.append(entry)

    # The current prompt — tell the agent to continue the discussion
    messages.append({
        "role": "user",
        "content": f"The current topic is: {topic}. Respond naturally, continuing the discussion.",
    })

    response = client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        temperature=0.8,
        max_tokens=150,
    )

    text = response.choices[0].message.content.strip()

    # Save to history so the OTHER agent sees this reply next turn
    # "assistant" = the agent who just spoke
    # "user"      = the other agent hearing it
    conversation_history.append({"role": "assistant", "content": text})

    return text


def reset_history():
    """Clear conversation history (e.g. when switching topics)."""
    conversation_history.clear()
