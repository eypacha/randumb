
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

## Technical details

This project includes several operational and developer-friendly features added during development:

- CORS support
   - Controlled via the `ALLOWED_ORIGINS` environment variable (comma-separated). Default: `*` (allows all origins).
   - Example: `ALLOWED_ORIGINS=https://example.com,https://app.example.com`

- Structured JSON logging
   - Uses `python-json-logger` and is configured in `app/logging.py`.
   - Log level can be controlled with the `LOG_LEVEL` env var (default: `INFO`).
   - Logs are emitted as JSON to stdout (suitable for structured log collectors).

- Health and readiness probes
   - Liveness: `GET /health` returns `{ "status": "ok" }`.
   - Readiness: `GET /ready` checks the SQLite DB connection and returns `200` when ready or `503` when not.

- OpenAPI / Swagger improvements
   - Tag descriptions for each resource are generated from `app/config/resources.py` and appear in the Swagger UI.
   - Each resource supports `singular` and `plural` fields in the config to produce friendly endpoint summaries (e.g. "Create a new pirate insult").

- Runtime feature flags
   - `ENABLE_CREATE` and `ENABLE_DELETE` (in `.env`) toggle POST/DELETE endpoints globally for all resources.

- Dev server helper
   - `devserver.sh` is a convenience script that will:
      - create a `.venv` if it doesn't exist,
      - activate the virtualenv,
      - upgrade `pip` and install `requirements.txt` (unless `NO_INSTALL=1`),
      - start `uvicorn app.main:app --reload --host 0.0.0.0`.
   - Usage:
      ```bash
      chmod +x devserver.sh
      ./devserver.sh
      # or skip install step
      NO_INSTALL=1 ./devserver.sh
      ```

- Pre-commit and formatting
   - `.pre-commit-config.yaml` is included with Black and basic hygiene hooks.
   - To enable locally:
      ```bash
      pip install pre-commit
      pre-commit install
      pre-commit run --all-files
      ```

- Requirements
   - `requirements.txt` includes `python-json-logger` for JSON logs. Install with:
      ```bash
      pip install -r requirements.txt
      ```

If you'd like, I can also add a short example of a JSON log line to the README, or include recommended production settings (restricting `ALLOWED_ORIGINS`, a Dockerfile, or sample systemd/Procfile configs).
