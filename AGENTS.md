# Meteo Tartufai — AGENTS.md

Early-stage weather tracking app for truffle hunters. Backend scaffolded with a growing CLI, no frontend yet.

## Quick start

```bash
docker compose up --build          # full stack (db + backend on :8000)
docker compose watch               # dev with hot reload (v2.23+)
```

No `.env` needed for dev — defaults work.

## Current state

- **Backend scaffolded** — `app/` has empty modules (models, routers, schemas, services — just `__init__.py`). `config.py` exists with only `from pydantic_settings import BaseSettings`.
- **CLI** — developed inside `backend/app/cli/` using **Typer**. Run via `docker compose exec backend python -m app.cli.main <command>`.
- **Frontend** — does not exist. `frontend` service is **commented out** in `docker-compose.yml`.
- **Alembic** — initialized in `backend/`, no migrations yet.
- **Tests** — none. Expected framework: `pytest` + `pytest-asyncio` + `httpx`.
- **CI / pre-commit / lint** — none configured.

## Architecture

```
backend/                    # FastAPI (Python 3.12) + CLI
├── app/
│   ├── cli/                # Typer CLI commands (shared services layer)
│   │   ├── main.py              # Entry point: Typer app, subcommand registration
│   │   ├── db_commands.py       # db: migrate, rollback, status
│   │   ├── meteo_commands.py    # meteo: import, fetch, validate (stub)
│   │   └── report_commands.py   # report: generate, export (stub)
│   ├── config.py           # Pydantic BaseSettings (single line)
│   ├── models/             # SQLAlchemy models (empty stub)
│   ├── schemas/            # Pydantic schemas (empty stub)
│   ├── routers/            # FastAPI routers (empty stub)
│   └── services/           # Business logic (empty stub)
├── alembic/                # Migration tool (initialized, no migrations)
├── requirements.txt
└── Dockerfile
frontend/                   # NOT YET CREATED (commented out of docker-compose)
docker-compose.yml          # PostGIS + backend only (frontend commented out)
docs/project/stack-reference.md     # Detailed tech docs
docs/project/opencode-workflow.md   # OpenCode workflow and agent operating rules
.opencode/project-context.md  # Agent context
.opencode/project_ideas/PRD.md  # Product requirements
```

### CLI

The CLI reuses the same services/models layer as FastAPI — different entry point, same business logic.

```bash
# Run via docker compose exec (container must be running)
docker compose exec backend python -m app.cli.main --help
docker compose exec backend python -m app.cli.main db migrate "add spots"
docker compose exec backend python -m app.cli.main db status
```

For ergonomic use, define an alias (inside WSL):
```bash
echo 'alias meteo-cli="docker compose exec backend python -m app.cli.main"' >> ~/.zshrc
source ~/.zshrc
meteo-cli db --help
```

- CLI entry point is **not** in the Docker CMD/ENTRYPOINT — container starts FastAPI normally, CLI is used via `exec`.
- Subcommands defined so far: `db` (migrate, rollback, status). `meteo` and `report` are stubs.
- `typer` added to `requirements.txt`.

### Stack details

- API prefix: `/api/`
- DB: PostgreSQL + PostGIS (`postgis/postgis:16-3.4`)
- ORM: SQLAlchemy 2.0 async + GeoAlchemy2
- Auth: JWT (python-jose), password hashing with argon2 (pwdlib)
- Auth tokens: 30min default expiry, OAuth2PasswordBearer at `/api/auth/login`
- Weather: Open-Meteo API (free, no key needed)

## Conventions

- **Language**: project docs and comments are in **Italian**
- **No comments in code** unless explicitly requested
- Backend: Pydantic schemas never expose DB models; services separate from routers; FastAPI dependencies for auth/DB
- CLI: Typer with type hints; subcommands grouped by domain (`db`, `meteo`, `report`)
- Frontend (future): TypeScript strict mode, Tailwind utility classes, function components with hooks, React Context or Zustand for state
- DB: `created_at` / `updated_at` on every table, PostGIS for spatial data
- `requirements.txt` has lines 1-10 and 13-22 duplicated — **intentional** for Docker layer caching

## Known gotchas

- `docker compose` (v2), **not** `docker-compose` (v1)
- `docker compose watch` requires Docker Compose v2.23+
- **Frontend service is commented out** in `docker-compose.yml`. Build fails if uncommented before `frontend/` exists.
- **Windows PowerShell users**: `grep`, `source`, and Unix pipes don't work. Use `findstr` instead of `grep`, or enter WSL with `wsl`.
- Backend `.vscode/.prettierrc` sets tabWidth:2, no tabs
- `.opencode/.gitignore` excludes itself + `node_modules` + `package.json` — these are not tracked
- Open-Meteo archive (ERA5) covers from 1940; forecast gives 7 days
- Alembic is initialized but has no migrations. First run: `alembic revision --autogenerate -m "init"` then `alembic upgrade head`.

## OpenCode workflow

This project follows the manual workflow defined in `docs/project/opencode-workflow.md`. That document is the authoritative reference for the two workflows, agent roles, artefact structure and handoffs. OpenCode acts as a consultant: it analyses, interviews, proposes and verifies; the developer writes the code.

Binding operating rules for every session:

- **Code changes require explicit user approval.** OpenCode prepares a short proposal covering what to change, where, expected behaviour and suggested verification. It does not apply code patches without approval. A failing test receives a diagnosis before any proposed fix.
- **Permissions differ by activity.** Repository analysis and verification commands may run directly. Configuration and plan changes may be applied directly. Existing documentation may be updated only after an adaptive interview. New documentation files require a proposal explaining their purpose, necessity and why an existing artefact is insufficient.
- **Interviews precede official artefact updates.** The interview depth adapts to ambiguity, risk, architectural impact and dependencies. It ends only after OpenCode presents a summary and the user explicitly confirms it; without confirmation, no official artefact is created or updated.
- **Conflicts stop the flow.** If a proposal conflicts with a previous artefact, OpenCode describes the conflict and asks for a decision instead of resolving it autonomously.
- **Handoffs are manual.** Each step produces its expected artefact and reports the result, open questions and next suggested agent or mandate. OpenCode never activates the next agent autonomously.
- **The workflow choice is explicit for each cycle.** Use Workflow A for specialist agents or Workflow B for generalist agents with an explicit mandate, at either macro-project or component scope. Detailed sequences, versioning rules and conceptual commands remain in `docs/project/opencode-workflow.md`.
