from app.extensions import get_db


PROMPTS_COLLECTION = "prompts"


def get_prompt_by_id(prompt_id):
    """Retrieve a prompt document by its _id."""
    db = get_db()
    return db[PROMPTS_COLLECTION].find_one({"_id": prompt_id})


def upsert_prompt(prompt_id, template):
    """Insert or update a prompt document."""
    db = get_db()
    result = db[PROMPTS_COLLECTION].update_one(
        {"_id": prompt_id},
        {"$set": {"template": template}},
        upsert=True,
    )
    return result
