# Intucate Case Study

A Flask-based application following the application factory pattern with a clean, maintainable architecture.

## Project Structure

```
intucate-case-study/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── config.py            # Environment configuration classes
│   ├── extensions.py        # Shared external clients/extensions
│   ├── routes/
│   │   ├── __init__.py
│   │   └── ask_routes.py    # API route blueprints
│   ├── services/
│   │   └── __init__.py      # Business/application logic
│   ├── repositories/
│   │   └── __init__.py      # MongoDB data access
│   └── utils/
│       ├── __init__.py
│       └── errors.py        # Error handling utilities
├── tests/
│   ├── __init__.py
│   └── test_health.py       # Health endpoint tests
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── pytest.ini
```

## Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
copy .env.example .env
```

## Running

```bash
python run.py
```

The server starts at `http://127.0.0.1:5000`.

## Testing

```bash
pytest
```
