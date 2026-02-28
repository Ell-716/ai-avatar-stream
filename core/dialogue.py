from groq import Groq
from groq import RateLimitError, APIError
from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_WINDOW, AGENTS
from utils.retry import retry_with_backoff
from logger import get_logger

logger = get_logger(__name__)
client = Groq(api_key=GROQ_API_KEY)

# Stores the full conversation so agents remember what was said
conversation_history: list[dict] = []


@retry_with_backoff(max_retries=3, base_delay=1, exceptions=(RateLimitError, APIError, Exception))
def generate_response(agent_key: str, topic: str) -> str:
    """
    Generate a response from the given agent using Groq.
    Maintains conversation context so the agent knows what was said before.

    Includes retry logic with exponential backoff for API failures.
    Returns a fallback response if all retries fail.
    """
    agent = AGENTS[agent_key]

    try:
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

        # Log context size for debugging
        context_size = len(conversation_history[-CONTEXT_WINDOW:])
        logger.debug(f"Generating response for {agent['name']} with {context_size} context messages")

        response = client.chat.completions.create(
            messages=messages,
            model=GROQ_MODEL,
            temperature=0.8,
            max_tokens=150,
        )

        text = response.choices[0].message.content.strip()

        logger.info(f"Generated response from {agent['name']} ({len(text)} chars)")

        # Save to history so the OTHER agent sees this reply next turn
        # "assistant" = the agent who just spoke
        # "user"      = the other agent hearing it
        conversation_history.append({"role": "assistant", "content": text})

        return text

    except RateLimitError as e:
        logger.warning(f"Rate limit hit for {agent['name']}: {e}")
        raise  # Let retry decorator handle it

    except APIError as e:
        logger.error(f"Groq API error for {agent['name']}: {e}")
        # Return fallback response instead of crashing
        fallback = "I need a moment to think about that."
        conversation_history.append({"role": "assistant", "content": fallback})
        return fallback

    except Exception as e:
        logger.error(f"Unexpected error generating response for {agent['name']}: {e}")
        # Return fallback response
        fallback = "I need a moment to think about that."
        conversation_history.append({"role": "assistant", "content": fallback})
        return fallback


def reset_history():
    """Clear conversation history (e.g. when switching topics)."""
    conversation_history.clear()
    logger.debug("Conversation history cleared")
