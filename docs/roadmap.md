# Roadmap Meteo Tartufai — da 0 a MVP

> Obiettivo finale: applicazione di tracciamento precipitazioni per tartufai (auth JWT, spot GPS, dati Open-Meteo, dashboard).
> Questo file è il punto di riferimento di ogni sessione. Aggiorna gli step con ✅ quando completati.

## Regole di avanzamento

1. **Un passo alla volta** — non si avanza finché lo step corrente non è compreso e testato.
2. **TDD sempre** — test prima del codice.
3. **Ogni step ha la struttura**: concetto → analisi → esercizio pratico.
4. **Alla fine di ogni fase** — verifica che tutto funzioni insieme (`docker compose up`).

---

## Fase 0: Fondamenta (DB & Config)

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 0.1 | `database.py` | Engine + sessione asincrona SQLAlchemy | async engine, sessionmaker, DeclarativeBase | ✅ |
| 0.2 | `config.py` completo | Settings Pydantic (DATABASE_URL, SECRET_KEY) | pydantic-settings, env var | ⬜ |
| 0.3 | Modello `User` | Tabella `users` | Mapped/mapped_column, hashing | ⬜ |

## Fase 1: Database & Migrazioni

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 1.1 | Modello `Spot` | Tabella `spots` con geometria | GeoAlchemy2, Geometry POINT | ⬜ |
| 1.2 | Prima migrazione Alembic | Tabelle reali nel DB | alembic revision/upgrade | ⬜ |
| 1.3 | Test DB con pytest | Connessione e CRUD verificati | pytest-asyncio, fixture | ⬜ |

## Fase 2: Services (Business Logic)

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 2.1 | Service `auth` | Registrazione + login + hash | pwdlib, argon2 | ⬜ |
| 2.2 | Service `spots` | CRUD completo con query spaziali | ST_DWithin, select async | ⬜ |
| 2.3 | Service `meteo` | Fetch Open-Meteo + salvataggio | httpx async, parsing | ⬜ |

## Fase 3: API (Routers FastAPI)

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 3.1 | Router `auth` | `/api/auth/register`, `/api/auth/login` | OAuth2PasswordBearer, JWT | ⬜ |
| 3.2 | Router `spots` | CRUD `/api/spots/*` | dependency injection, Pydantic schemas | ⬜ |
| 3.3 | Router `meteo` | `/api/spots/{id}/refresh`, dati storici | BackgroundTasks | ⬜ |
| 3.4 | `main.py` | App FastAPI completa con router | include_router, prefix | ⬜ |

## Fase 4: Auth & Sicurezza

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 4.1 | `dependencies.py` | `get_current_user`, `get_db` | Depends, OAuth2, errori 401 | ⬜ |
| 4.2 | Protezione endpoint | Solo utenti autenticati accedono ai propri spot | ownership check | ⬜ |

## Fase 5: Frontend (React + Vite + Tailwind)

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 5.1 | Setup Vite + Tailwind | Progetto frontend in `frontend/` | `npm create vite`, tailwind | ⬜ |
| 5.2 | Mappa MapLibre | Mappa con spot salvati | maplibre-gl, marker | ⬜ |
| 5.3 | Auth UI | Login/registrazione | React state, fetch | ⬜ |
| 5.4 | Dashboard grafici | Precipitazioni con Recharts | LineChart, BarChart | ⬜ |
| 5.5 | Heatmap | Overlay precipitazioni | heatmap layer MapLibre | ⬜ |
| 5.6 | Docker compose frontend | Unico `docker compose up` | build frontend, proxy | ⬜ |

## Fase 6: CLI (Collegare lo scheletro esistente)

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 6.1 | `db status` funzionante | Stato migrazioni reali | Typer + Alembic API | ⬜ |
| 6.2 | `meteo import` | Import batch dati meteo | services riusati dalla CLI | ⬜ |
| 6.3 | `report generate` | Report PDF/JSON | export, formattazione | ⬜ |

## Fase 7: Test & Qualità

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 7.1 | Test unitari services | Copertura auth, spots, meteo | pytest, mock httpx | ⬜ |
| 7.2 | Test API | Endpoint verificati end-to-end | httpx AsyncClient, TestClient | ⬜ |
| 7.3 | CI + pre-commit | Lint, typecheck, test automatici | ruff, pre-commit | ⬜ |

## Fase 8: Produzione (Optional)

| Step | Obiettivo | Deliverable | Conoscenze chiave | Stato |
|---|---|---|---|---|
| 8.1 | Deploy VPS | Docker Compose prod | Nginx, Let's Encrypt | ⬜ |
| 8.2 | Backup & monitoraggio | Restore, healthcheck | cron, pg_dump | ⬜ |

---

## Stato attuale progetto (al fork sessione)

- Backend scaffoldato FastAPI (moduli vuoti)
- CLI scheletro Typer in `backend/app/cli/` (comandi `pass`)
- Nessun modello, nessuna migrazione, nessun test
- `docker-compose.yml`: db + backend attivi, frontend commentato
- Documentazione: `docs/stack-reference.md`, `AGENTS.md`, `.opencode/project-context.md`

## Note di contesto

- Livello utente: conosce un po' di PostgreSQL, poco SQLAlchemy → gli step 0-1 saranno più lenti e ricchi di spiegazioni
- Trucchetti accumulati in `docs/tricks.md` (aggiornare a ogni step)
- Convenzioni: codice/documenti in italiano, niente commenti nel codice, TDD
- Stack: FastAPI + SQLAlchemy 2.0 async + GeoAlchemy2 + Alembic + pytest + React/Vite/Tailwind + MapLibre + Recharts + Open-Meteo + Docker Compose
