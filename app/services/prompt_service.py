from app.repositories import prompt_repository
from app.utils.errors import AppError

EDUCATION_PROMPT_ID = "Education_Prompt"
PLACEHOLDER = "{{userInput}}"


def build_prompt(user_input):
    """Retrieve the Education_Prompt template and replace the placeholder with user input."""
    doc = prompt_repository.get_prompt_by_id(EDUCATION_PROMPT_ID)

    if doc is None:
        raise AppError("Education_Prompt not found", status_code=500)

    template = doc["template"]
    return template.replace(PLACEHOLDER, user_input)
