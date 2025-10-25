
# Randumb API

A modular FastAPI API for generating and managing random dumb things, such as pirate insults and excuses. Built with FastAPI, SQLite, Pydantic, and designed for easy extension to new resources.

## Features

- Modular architecture with dynamic resource generation
- Pagination support for list endpoints
- Environment-based endpoint control for production
- SQLite database with automatic table initialization
- Swagger UI documentation

## Quick Start

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Copy the environment file:
   ```sh
   cp .env.example .env
   ```

3. Run the server:
   ```sh
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`.

## Development: Black & pre-commit

This repository includes a `.pre-commit-config.yaml` that runs Black (the Python formatter)
and some basic hygiene hooks before each commit. To enable the hooks locally:

```bash
pip install pre-commit
pre-commit install
# optional: run against all files once
pre-commit run --all-files
```

Black configuration is in `pyproject.toml`.

## Endpoints

The API dynamically generates endpoints for each configured resource. Currently supported resources:

### Pirates
- `POST /pirates/` — Create a new pirate insult
- `GET /pirates/?page=1&limit=10` — List pirate insults with pagination
- `DELETE /pirates/` — Delete multiple pirate insults

### Excuses
- `POST /excuses/` — Create a new excuse
- `GET /excuses/?page=1&limit=10` — List excuses with pagination
- `DELETE /excuses/` — Delete multiple excuses

## Configuration

Resources are defined in `app/config/resources.py`. Add new resources there to extend the API.

Environment variables in `.env`:
- `ENABLE_CREATE`: Enable/disable POST endpoints for all resources
- `ENABLE_DELETE`: Enable/disable DELETE endpoints for all resources

## Project Structure

- `app/config/` — Resource configurations
- `app/routes/` — Dynamic router generation
- `app/functions/` — Generic CRUD operations
- `app/schemas/` — Pydantic models (generated dynamically)
- `app/main.py` — Application entry point
- `requirements.txt` — Python dependencies
- `pyproject.toml` — Black formatter configuration
