"""Seed the required Education_Prompt document into MongoDB.

Usage:
    py scripts/seed_prompts.py

Requires MONGODB_URI and MONGODB_DATABASE environment variables
(or a .env file in the project root).
"""

import os
from urllib.parse import urlparse, urlunparse, quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient


PROMPT_ID = "Education_Prompt"
PROMPT_TEMPLATE = "You are an expert in education domain. Answer the following: {{userInput}}"


def _encode_uri(uri):
    """URL-encode username and password in a MongoDB connection string."""
    parsed = urlparse(uri)
    if parsed.username or parsed.password:
        user = quote_plus(parsed.username) if parsed.username else ""
        passwd = quote_plus(parsed.password) if parsed.password else ""
        netloc = f"{user}:{passwd}@{parsed.hostname}"
        if parsed.port:
            netloc += f":{parsed.port}"
        return urlunparse(parsed._replace(netloc=netloc))
    return uri


def seed():
    load_dotenv()

    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DATABASE", "intucate")

    client = MongoClient(_encode_uri(uri))
    db = client[db_name]

    result = db.prompts.update_one(
        {"_id": PROMPT_ID},
        {"$set": {"template": PROMPT_TEMPLATE}},
        upsert=True,
    )

    if result.upserted_id:
        print(f"Inserted '{PROMPT_ID}' prompt.")
    elif result.modified_count:
        print(f"Updated '{PROMPT_ID}' prompt.")
    else:
        print(f"'{PROMPT_ID}' prompt already exists and is up to date.")

    client.close()


if __name__ == "__main__":
    seed()
