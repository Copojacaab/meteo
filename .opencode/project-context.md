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
│   │   ├── main.py             # FastAPI app e /api/health
│   │   ├── cli/
│   │   ├── models/
│   │   │   └── user.py          # User model confirmed in Phase 2
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── services/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── tests/
│   ├── alembic.ini
│   ├── alembic/
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

## Regole per il consulente

- Per decisioni su librerie/framework, consultare `docs/project/stack-reference.md`
- Per lo stato del progetto e roadmap, consultare `docs/project/roadmap.md` e `.opencode/project_ideas/PRD.md`
- Usare Context7 per fetchare documentazione aggiornata quando necessario
- Seguire le convenzioni specificate in `docs/project/stack-reference.md#9-convenzioni-di-progetto`
- `backend/app/models/user.py` è stato confermato nella Fase 2; le modifiche future devono rispettare il modello e passare dalla roadmap.
- Il codice deve restare semplice e didattico; i commenti sono consentiti quando spiegano un concetto, un comando o una decisione non ovvia.
- I piani sono guide operative per l'utente umano: devono includere concetti, file, comandi scomposti, risultati attesi e punti in cui chiedere aiuto.
- L'utente implementa personalmente il codice. Il consulente spiega, propone, diagnostica e verifica; non attiva worker automatici e non presume l'uso di `$start-work`.
- Prima di scrivere codice, leggere i file esistenti per capire lo stile
