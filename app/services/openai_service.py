from openai import OpenAI
from app.utils.errors import AppError

_client = None


def get_client():
    """Return a lazily initialized OpenAI client."""
    global _client
    if _client is None:
        from flask import current_app
        api_key = current_app.config.get("OPENAI_API_KEY")
        if not api_key:
            raise AppError("OpenAI API key not configured", status_code=500)
        _client = OpenAI(api_key=api_key)
    return _client


def get_chat_response(prompt):
    """Send a prompt to OpenAI and return the assistant's response text."""
    client = get_client()

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception:
        raise AppError("Failed to get response from OpenAI", status_code=502)
