# Session Data — Creazione CLI Meteo Tartufai

## Data
2026-07-30

## Obiettivo
Creare una CLI per il progetto Meteo Tartufai usando Typer (Python), integrata dentro il backend FastAPI esistente.

## Roadmap completata (Fase 1)

### Step 1: Setup Architettura & CLI Boilerplate
- [x] Analisi del progetto esistente e necessità della CLI
- [x] Creazione struttura `backend/app/cli/`
- [x] Implementazione `main.py` (entry point Typer)
- [x] Implementazione `db_commands.py` (migrate, rollback, status — con `pass`)
- [x] Implementazione `meteo_commands.py` (app creata, zero comandi — stub)
- [x] Implementazione `report_commands.py` (solo docstring — stub)
- [x] Aggiunta `typer` a `requirements.txt`
- [x] Ricostruzione container Docker con nuova dipendenza

### Stato attuale dei file

```
backend/app/cli/
├── __init__.py            # Vuoto
├── main.py                # ✅ App Typer, registra db e meteo
├── db_commands.py         # ✅ 3 comandi (tutti pass)
├── meteo_commands.py      # ⚠️  App creata, 0 comandi
└── report_commands.py     # ❌ Solo docstring, non importato
```

Modifiche a file esistenti:
- `backend/requirements.txt` — aggiunto `typer`
- `docker-compose.yml` — servizio `frontend` commentato (non esiste ancora)
- `AGENTS.md` — aggiornato con sezione CLI, alias, gotchas

## Scoperte architetturali

### Come funziona la CLI
- La CLI **riusa gli stessi services/models** del backend FastAPI
- Non va nell'ENTRYPOINT del container (che resta FastAPI)
- Si usa via `docker compose exec backend python -m app.cli.main <comando>`
- Alternativa: alias `meteo-cli` in `.zshrc`

### Struttura Typer
- `main.py` crea `app = typer.Typer()` e registra sottogruppi con `app.add_typer()`
- Ogni file comandi crea un `typer.Typer()` separato (es: `db_app`, `meteo_app`)
- I comandi si registrano con `@db_app.command()` sopra la funzione
- Typer genera automaticamente `--help` dai docstring e type hints

### Docker
- `CMD` / `ENTRYPOINT` controllano cosa fa il container all'avvio
- `docker compose exec` esegue comandi dentro un container già vivo
- La CLI si usa con `exec`, non modifica l'avvio del container
- Layer caching: `requirements.txt` copiato prima del codice per build più veloci

## Difficoltà incontrate

### 1. Windows PowerShell vs Unix
- Comandi Unix (`grep`, `source`) non funzionano in PowerShell
- Soluzione: usare `findstr` o entrare in WSL con `wsl`
- Lezione: lavorare sempre in WSL per progetti con toolchain Unix

### 2. Docker compose da cartella sbagliata
- Lanciato `docker compose` da `backend/` invece che dalla root del progetto
- Il `docker-compose.yml` è nella root `/meteo/`, non in `/meteo/backend/`
- Soluzione: `cd ..` per tornare alla root

### 3. Frontend non esistente blocco il build
- Il servizio `frontend` in `docker-compose.yml` causava errore perché la directory non esiste
- Soluzione: commentare il servizio `frontend` nel compose

### 4. File CLI incompleti
- `meteo_commands.py` ha l'app ma nessun comando
- `report_commands.py` è solo una docstring, non importato in `main.py`
- Da completare negli step successivi

## Decisioni architetturali

| Decisione | Motivazione |
|---|---|
| CLI dentro `backend/app/cli/` | Condivide dipendenze e layer services col backend |
| Nessun ENTRYPOINT dedicato | Il container deve restare un server FastAPI |
| Typer come framework CLI | Type hints nativi, auto-generazione help, pattern simile a FastAPI |
| Alias bash per uso frequente | Ergonomicamente migliore del comando Docker completo |
| `requirements.txt` duplicato intenzionale | Docker layer caching (primo layer: dipendenze, secondo: codice) |

## Prossimi passi (suggeriti)

1. Completare `meteo_commands.py` con comandi reali (import, fetch, validate)
2. Completare `report_commands.py` e registrarlo in `main.py`
3. Sostituire `pass` con logica reale in `db_commands.py`
4. Aggiungere testing con `pytest`
5. Configurare CI / pre-commit
