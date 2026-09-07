from openai import OpenAI, AsyncOpenAI
from app.utils.errors import AppError

_client = None
_async_client = None


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


def get_async_client():
    """Return a lazily initialized async OpenAI client."""
    global _async_client
    if _async_client is None:
        from flask import current_app
        api_key = current_app.config.get("OPENAI_API_KEY")
        if not api_key:
            raise AppError("OpenAI API key not configured", status_code=500)
        _async_client = AsyncOpenAI(api_key=api_key)
    return _async_client


def get_chat_response(prompt):
    """Send a prompt to OpenAI and return the assistant's response text."""
    client = get_client()

    from flask import current_app
    model = current_app.config.get("OPENAI_MODEL", "gpt-3.5-turbo")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception:
        raise AppError("Failed to get response from OpenAI", status_code=502)


async def get_chat_response_async(prompt):
    """Send a prompt to OpenAI asynchronously and return the assistant's response text."""
    client = get_async_client()

    from flask import current_app
    model = current_app.config.get("OPENAI_MODEL", "gpt-3.5-turbo")

    try:
        completion = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception:
        raise AppError("Failed to get response from OpenAI", status_code=502)
