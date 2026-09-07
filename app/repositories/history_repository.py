from datetime import datetime, timezone

from app.extensions import get_db


HISTORY_COLLECTION = "history"


def insert_history(user_input, response):
    """Insert a request/response pair into the history collection."""
    db = get_db()
    doc = {
        "userInput": user_input,
        "response": response,
        "createdAt": datetime.now(timezone.utc),
    }
    result = db[HISTORY_COLLECTION].insert_one(doc)
    return result.inserted_id
