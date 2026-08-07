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
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── services/
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/
│   └── stack-reference.md    # Documentazione tecnica dettagliata
├── docker-compose.yml
├── PRD.md                    # Requisiti di progetto
└── .opencode/
    └── project-context.md    # Questo file
```

## Roadmap MVP

1. **Sprint 1:** Docker Compose, auth JWT, modello User
2. **Sprint 2:** Modello Spot (PostGIS), CRUD spot, mappa
3. **Sprint 3:** Open-Meteo API, aggiornamento dati meteo
4. **Sprint 4:** Dashboard grafici, heatmap precipitazioni

## Regole per l'agente

- Per decisioni su librerie/framework, consultare `docs/project/stack-reference.md`
- Per lo stato del progetto e roadmap, consultare `PRD.md` e questo file
- Usare Context7 per fetchare documentazione aggiornata quando necessario
- Seguire le convenzioni specificate in `docs/project/stack-reference.md#9-convenzioni-di-progetto`
- **Non aggiungere commenti al codice** (tranne se esplicitamente richiesto)
- Prima di scrivere codice, leggere i file esistenti per capire lo stile
