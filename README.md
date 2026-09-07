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
│   │   └── ask_routes.py        # API route blueprints (/health, /ask, /ask/batch)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prompt_service.py    # Prompt construction logic
│   │   ├── openai_service.py    # OpenAI API communication
│   │   ├── history_service.py   # History orchestration
│   │   └── batch_service.py     # Async batch processing
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── prompt_repository.py # MongoDB prompt data access
│   │   └── history_repository.py# MongoDB history data access
│   └── utils/
│       ├── __init__.py
│       └── errors.py            # Error handling utilities
├── scripts/
│   ├── __init__.py
│   └── seed_prompts.py          # Seed Education_Prompt into MongoDB
├── tests/
│   ├── __init__.py
│   ├── test_health.py           # Health endpoint tests
│   ├── test_ask.py              # /ask endpoint tests
│   ├── test_batch.py            # /ask/batch endpoint tests
│   ├── test_prompt_repository.py# Prompt repository unit tests
│   ├── test_prompt_service.py   # Prompt service unit tests
│   ├── test_history_repository.py# History repository unit tests
│   └── test_history_service.py  # History service unit tests
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── run.py
└── pytest.ini
```

## Setup

### Prerequisites

- Python 3.10+
- MongoDB (local installation or [MongoDB Atlas](https://www.mongodb.com/atlas))
- OpenAI API key

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

Edit `.env` with your configuration:

```
SECRET_KEY=your-secret-key
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=intucate
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

For MongoDB Atlas:

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/ask` | Single prompt → OpenAI response |
| POST | `/ask/batch` | Batch prompt → concurrent OpenAI responses |

### POST /ask

```json
// Request
{ "userInput": "What is Python?" }

// Response
{ "response": "Python is a high-level programming language..." }
```

### POST /ask/batch

```json
// Request
{ "userInputs": ["What is Python?", "What is MongoDB?"] }

// Response
{ "responses": ["Python is...", "MongoDB is..."] }
```

## Testing

```bash
py -m pytest -v
```

All tests use mocked MongoDB and OpenAI — no live connections required.
