# Meteo Tartufai — AGENTS.md

Early-stage weather tracking app for truffle hunters. Backend scaffolded with a growing CLI, no frontend yet.

## Quick start

I comandi sono intenzionalmente separati per rendere visibile cosa succede.

```bash
# Costruisce l'immagine del backend leggendo backend/requirements.txt
docker compose build backend

# Avvia database e backend e mostra i log nel terminale
docker compose up
```

Per lasciare i servizi in background:

```bash
docker compose up -d
```

`docker compose build backend` costruisce l'immagine del backend. `docker compose up` crea e avvia i servizi definiti in `docker-compose.yml`. L'opzione `-d` significa "detached": i container restano attivi senza occupare il terminale.

No `.env` needed for dev — defaults work.

## Current state

- **Backend baseline** — `config.py` and `database.py` contain the settings and async database infrastructure. `app/main.py` exposes `/api/health` and the auth router. `models/user.py` defines the persisted User model; auth schemas, service, router and current-user dependency are implemented.
- **CLI** — developed inside `backend/app/cli/` using **Typer**. Run via `docker compose exec backend python -m app.cli.main <command>`.
- **Frontend** — does not exist. `frontend` service is **commented out** in `docker-compose.yml`.
- **Alembic** — initialized in `backend/alembic/` with `backend/alembic.ini`; the `users` migration is applied.
- **Tests** — baseline and auth suite configured in `backend/pytest.ini` and `backend/tests/`; framework: `pytest` + `pytest-asyncio` + `httpx`; 23 tests pass in Compose.
- **CI / pre-commit / lint** — none configured.
- **Roadmap** — `docs/project/roadmap.md` is the single source of truth for development phases and status.

## Architecture

```
backend/                    # FastAPI (Python 3.12) + CLI
├── app/
│   ├── cli/                # Typer CLI commands (shared services layer)
│   │   ├── main.py              # Entry point: Typer app, subcommand registration
│   │   ├── db_commands.py       # db: migrate, rollback, status
│   │   ├── meteo_commands.py    # gruppo meteo registrato, senza comandi
│   │   └── report_commands.py   # stub non ancora registrato
│   ├── config.py           # Pydantic settings
│   ├── database.py         # Async engine, session factory and DeclarativeBase
│   ├── models/             # SQLAlchemy models; user.py is a walking skeleton
│   ├── schemas/            # Pydantic API schemas
│   ├── routers/            # FastAPI routers and auth dependencies
│   └── services/           # Business logic, including auth
├── alembic/                # Async migrations; users migration present
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
- Subcommands defined so far: `db` (three placeholder commands). `meteo` is registered without commands, and `report` is not registered.
- `typer` added to `requirements.txt`.

### Stack details

Questi strumenti hanno ruoli diversi:

- **Docker** crea ambienti isolati per eseguire i programmi.
- **Docker Compose** coordina più container: in questo progetto il database `db` e il backend `backend`.
- **FastAPI** definisce l'API HTTP usando funzioni Python.
- **Uvicorn** esegue l'app FastAPI come server ASGI.
- **pytest** esegue i test automatici.
- **pytest-asyncio** permette a pytest di eseguire funzioni `async def`.
- **httpx** permette ai test di chiamare l'API.
- **SQLAlchemy** collega classi Python e tabelle SQL.
- **Alembic** registra le modifiche allo schema del database tramite migrazioni.
- **PostgreSQL** conserva i dati; **PostGIS** aggiunge i dati geografici.

Quando si studia un nuovo strumento, il consulente deve prima spiegarne il ruolo, poi mostrare la configurazione minima e infine collegarla al comando o al file che l'utente sta modificando.

- API prefix: `/api/`
- DB: PostgreSQL + PostGIS (`postgis/postgis:16-3.4`)
- ORM: SQLAlchemy 2.0 async + GeoAlchemy2
- Auth: JWT (python-jose), password hashing with argon2 (pwdlib)
- Auth tokens: 30min default expiry, OAuth2PasswordBearer at `/api/auth/login`
- Weather: Open-Meteo API (free, no key needed)

## Conventions

- **Language**: project docs and comments are in **Italian**
- **Codice semplice e didattico**: evitare astrazioni premature e percorsi alternativi non necessari. I commenti sono consentiti quando aiutano a capire un concetto nuovo, un comando Docker o una decisione non ovvia; non aggiungere commenti che ripetano semplicemente il codice.
- **TDD spiegato**: quando si usa TDD, spiegare prima il comportamento atteso, poi il test rosso, l'implementazione minima e il test verde.
- **Test spiegati**: `pytest.ini` configura la raccolta e l'esecuzione dei test; `conftest.py` contiene fixture condivise; `pytest.fixture` prepara valori riutilizzabili dai test. Prima di usarli, spiegarne il ruolo.
- Backend: Pydantic schemas never expose DB models; services separate from routers; FastAPI dependencies for auth/DB
- CLI: Typer with type hints; subcommands grouped by domain (`db`, `meteo`, `report`)
- Frontend (future): TypeScript strict mode, Tailwind utility classes, function components with hooks, React Context or Zustand for state
- DB: `created_at` / `updated_at` on every table, PostGIS for spatial data

## Known gotchas

- `docker compose` (v2), **not** `docker-compose` (v1)
- `docker compose watch` requires Docker Compose v2.23+
- **Frontend service is commented out** in `docker-compose.yml`. Build fails if uncommented before `frontend/` exists.
- **Windows PowerShell users**: `grep`, `source`, and Unix pipes don't work. Use `findstr` instead of `grep`, or enter WSL with `wsl`.
- Backend `.vscode/.prettierrc` sets tabWidth:2, no tabs
- `.opencode/.gitignore` excludes itself + `node_modules` + `package.json` — these are not tracked
- Open-Meteo archive (ERA5) covers from 1940; forecast gives 7 days
- Alembic is initialized. Generate and apply the first real migration only after the User-model gate and step 2.2.
- The backend exposes `/api/health` on host port 8000 after `docker compose up`; rebuild the backend image after source or dependency changes because Compose has no source volume mount.

## OpenCode workflow

This project follows the manual workflow defined in `docs/project/opencode-workflow.md`. That document is the authoritative reference for the two workflows, agent roles, artefact structure and handoffs. OpenCode acts as a consultant: it analyses, interviews, proposes and verifies; the developer writes the code.

I piani di lavoro sono guide operative per l'utente umano, non incarichi per worker automatici. Ogni piano deve essere leggibile anche da chi sta imparando e deve includere:

- obiettivo funzionale e obiettivo didattico dello step;
- concetti e strumenti utilizzati;
- file da leggere e modificare;
- comandi scomposti in passaggi semplici, con spiegazione delle opzioni;
- risultato atteso e criteri di verifica;
- punti in cui l'utente può chiedere spiegazioni, diagnosi o revisione del codice.

L'utente esegue personalmente l'implementazione. Il consulente aiuta a comprendere i concetti, analizzare gli errori, proporre codice e verificare il lavoro su richiesta. Non si deve presumere l'uso di `$start-work` o di un worker separato.

Binding operating rules for every session:

- **Code changes require explicit user approval.** OpenCode prepara una proposta breve che descrive cosa cambiare, dove, comportamento atteso e verifica suggerita. L'utente scrive e applica il codice; il consulente non deve applicare modifiche al prodotto al posto suo. Un test fallito riceve prima una diagnosi e una spiegazione.
- **Permissions differ by activity.** Repository analysis and verification commands may run directly. Configuration and plan changes may be applied directly. Existing documentation may be updated only after an adaptive interview. New documentation files require a proposal explaining their purpose, necessity and why an existing artefact is insufficient.
- **Interviews precede official artefact updates.** The interview depth adapts to ambiguity, risk, architectural impact and dependencies. It ends only after OpenCode presents a summary and the user explicitly confirms it; without confirmation, no official artefact is created or updated.
- **Conflicts stop the flow.** If a proposal conflicts with a previous artefact, OpenCode describes the conflict and asks for a decision instead of resolving it autonomously.
- **Handoffs are manual.** Ogni step produce il proprio risultato e riporta esito, domande aperte e prossimo argomento didattico suggerito. OpenCode non attiva automaticamente worker o agenti per implementare il codice.
- **The workflow choice is explicit for each cycle.** Use Workflow A for specialist agents or Workflow B for generalist agents with an explicit mandate, at either macro-project or component scope. Detailed sequences, versioning rules and conceptual commands remain in `docs/project/opencode-workflow.md`.
