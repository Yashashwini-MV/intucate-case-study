import asyncio

from app.services import prompt_service, openai_service, history_service
from app.utils.errors import AppError


async def _process_single(user_input):
    """Process a single input: build prompt, call OpenAI, save history."""
    prompt = prompt_service.build_prompt(user_input)
    response = await openai_service.get_chat_response_async(prompt)
    history_service.save_history(user_input, response)
    return response


async def process_batch(user_inputs):
    """Process a list of user inputs concurrently and return responses in order."""
    tasks = [_process_single(inp) for inp in user_inputs]
    return await asyncio.gather(*tasks)
