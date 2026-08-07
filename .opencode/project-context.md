# Meteo Tartufai — Project Context

## Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite + Tailwind CSS
- **Mappa:** MapLibre GL JS
- **DB:** PostgreSQL + PostGIS
- **ORM:** SQLAlchemy 2.0 async + GeoAlchemy2
- **Auth:** JWT (python-jose + pwdlib)
- **Meteo:** Open-Meteo API (no API key)
- **Grafici:** Recharts
- **Deploy:** Docker Compose

## Struttura repo

```
meteo/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── cli/
│   │   ├── models/
│   │   │   └── user.py          # walking skeleton; review postponed
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── docs/
│   └── project/
│       ├── roadmap.md
│       ├── stack-reference.md
│       └── opencode-workflow.md
├── docker-compose.yml
├── .opencode/project_ideas/PRD.md # Requisiti di progetto
└── .opencode/
    └── project-context.md    # Questo file
```

## Roadmap MVP

La fonte unica per fasi, dipendenze, criteri di accettazione e stato è `docs/project/roadmap.md`. La roadmap traduce gli sprint MVP del PRD in passi verificabili.

## Regole per l'agente

- Per decisioni su librerie/framework, consultare `docs/project/stack-reference.md`
- Per lo stato del progetto e roadmap, consultare `docs/project/roadmap.md` e `.opencode/project_ideas/PRD.md`
- Usare Context7 per fetchare documentazione aggiornata quando necessario
- Seguire le convenzioni specificate in `docs/project/stack-reference.md#9-convenzioni-di-progetto`
- Non estendere `backend/app/models/user.py`: l'analisi del modello è rinviata su richiesta dell'utente e costituisce un gate della roadmap.
- **Non aggiungere commenti al codice** (tranne se esplicitamente richiesto)
- Prima di scrivere codice, leggere i file esistenti per capire lo stile
