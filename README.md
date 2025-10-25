
# Randumb API

Example API using FastAPI, SQLite, and Pydantic for random dumb things.

This project is designed to let you create and retrieve random silly content, starting with pirate insults, but easily extendable to any other kind of random fun data.

## Quick Start

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the server (from the project root):
   ```sh
   uvicorn app.main:app --reload
   ```

## Endpoints

- `POST /pirates/` — Add a pirate insult (example resource)
- `GET /pirates/` — List all pirate insults

## Structure

- `app/models/` — Database models (ready to grow)
- `app/schemas/` — Pydantic schemas (see `pirates.py`)
- `app/functions/` — Business logic and data access (see `pirates.py`)
- `app/routes/` — API endpoints (see `pirates.py`)
- `app/main.py` — Application entry point

The root folder contains only configuration and documentation files.
