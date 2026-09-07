from app.repositories import history_repository


def save_history(user_input, response):
    """Save a successful request/response pair to history."""
    return history_repository.insert_history(user_input, response)
