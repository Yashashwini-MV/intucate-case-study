# Intucate Case Study

A Flask-based application following the application factory pattern with a clean, maintainable architecture.

## Project Structure

```
intucate-case-study/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── config.py                # Environment configuration classes
│   ├── extensions.py            # Shared external clients/extensions (MongoDB)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── ask_routes.py        # API route blueprints
│   ├── services/
│   │   └── __init__.py          # Business/application logic
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── prompt_repository.py # MongoDB prompt data access
│   └── utils/
│       ├── __init__.py
│       └── errors.py            # Error handling utilities
├── scripts/
│   ├── __init__.py
│   └── seed_prompts.py          # Seed Education_Prompt into MongoDB
├── tests/
│   ├── __init__.py
│   ├── test_health.py           # Health endpoint tests
│   └── test_prompt_repository.py # Prompt repository unit tests
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── pytest.ini
```

## Setup

### Prerequisites

- Python 3.10+
- MongoDB (local installation or [MongoDB Atlas](https://www.mongodb.com/atlas))

### Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

### Environment Variables

Edit `.env` with your MongoDB connection details:

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=intucate
```

For MongoDB Atlas, use your cluster connection string:

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
MONGODB_DATABASE=intucate
```

### Seed the Education Prompt

```bash
py scripts/seed_prompts.py
```

This upserts the required prompt document:

```json
{
    "_id": "Education_Prompt",
    "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}
```

Safe to run multiple times (uses upsert).

## Running

```bash
python run.py
```

The server starts at `http://127.0.0.1:5000`.

## Testing

```bash
py -m pytest -v
```

Unit tests for the prompt repository use mocked MongoDB and do not require a running database.

Integration tests (if added later) will require a live MongoDB connection and will be clearly marked.
