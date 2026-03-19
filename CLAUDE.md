# CLAUDE.md

## Project Overview

`trello_move` is a Python automation tool that resets daily Trello boards by moving all cards from "doing" and "done" lists back to "todo" at a scheduled time. It targets boards named "tasks" belonging to organizations with "family" in the name.

## Development Setup

Uses `uv` as the package manager:

```bash
uv sync
```

Environment variables are loaded from an `.env` file (gitignored):
```
TRELLO_API_KEY=...
TRELLO_API_SECRET=...
```

## Running the Application

```bash
# Run immediately (one-shot card move)
uv run python trello_main.py

# Run the scheduler service (executes card move daily at 4:00 AM)
uv run python trello_service.py

# Run the scheduler but execute immediately (bypass schedule)
uv run python trello_service.py --now
```

## Docker

```bash
docker-compose up --build
```

The container passes `TRELLO_API_KEY` and `TRELLO_API_SECRET` from the host environment and uses an external Docker network named `app`.

## Architecture

Two-module design:

- **`trello_service.py`** — Scheduler loop. Polls every 10 seconds, triggers `main()` from `trello_main.py` when `hour == 4` and `minute == 0`. Supports `--now` flag to skip the wait.
- **`trello_main.py`** — Business logic. Authenticates with the Trello API, finds all boards named "tasks" under "family" organizations, identifies each board's "todo" list (case-insensitive, ignoring spaces), and moves all cards from other lists into it.

**List protection:** Lists whose names start with `_` are skipped and their cards are never moved.

**Note on schedule discrepancy:** `trello_service.py` triggers at 4:00 AM (`MOVE_HOUR = 4`), while the systemd timer (`trello.timer`) fires at 6:00 AM. The systemd setup runs `trello_main.py` directly (bypassing the service scheduler), so the two schedules don't conflict.

## Code Style

Use comments sparingly. Only comment complex code.

## Deployment Options

- **Raspberry Pi / systemd:** Use `trello.service` + `trello.timer`. The service file still references `poetry run` — update if needed.
- **Docker Compose:** `docker-compose.yml` with restart policy `always`.
- **Portainer stacks:** `captain-definition` points to the Dockerfile.
