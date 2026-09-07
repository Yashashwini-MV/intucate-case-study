from urllib.parse import urlparse, urlunparse, quote_plus

from pymongo import MongoClient

mongo_client = None
mongo_db = None


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


def init_mongo(app):
    """Initialize MongoDB connection from Flask app config."""
    global mongo_client, mongo_db

    uri = app.config["MONGODB_URI"]
    db_name = app.config["MONGODB_DATABASE"]

    mongo_client = MongoClient(_encode_uri(uri))
    mongo_db = mongo_client[db_name]

    app.mongo_client = mongo_client
    app.mongo_db = mongo_db


def get_db():
    """Return the active MongoDB database instance."""
    if mongo_db is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongo() first.")
    return mongo_db
