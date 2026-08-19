# Roadmap Meteo Tartufai — da 0 a MVP

> Obiettivo MVP: applicazione per monitorare precipitazioni e condizioni meteo di spot privati, con autenticazione, mappa, dati Open-Meteo e dashboard.
> Questo file è la fonte unica di verità per fasi, dipendenze, criteri di accettazione e stato del progetto.

## Regole di avanzamento

1. Un passo alla volta: non si avanza finché lo step corrente non è compreso, implementato e verificato.
2. TDD: il test viene definito prima dell'implementazione, quando il livello del componente lo consente.
3. Ogni step segue il ciclo: concetto, analisi, esercizio o implementazione, verifica.
4. Alla fine di ogni fase si verifica l'integrazione disponibile con `docker compose up --build`.
5. Le funzionalità di notifiche, diario, fenologia e IoT sono fuori scope per questa MVP.

## Stato attuale verificato

| Elemento | Stato | Nota |
|---|---|---|
| `database.py` | ✅ | Engine async, session factory, `Base` e `get_db` presenti |
| `config.py` | ✅ | Settings con URL DB, secret e scadenza JWT da ambiente |
| `models/user.py` | ✅ | Modello confermato con email unica, hash password e timestamp |
| `app/main.py` | ✅ | App FastAPI con healthcheck e router auth registrato |
| Alembic | ✅ | Ambiente async configurato; migrazione `users` applicata |
| CLI | ⬜ | Scheletro Typer con comandi DB placeholder |
| Test | ✅ | pytest + pytest-asyncio configurati; suite baseline e auth verde |
| Frontend | ⬜ | Non ancora creato; servizio Compose commentato |

## Fase 1 — Baseline eseguibile

Questa fase rende verificabile lo scaffold e prepara il lavoro applicativo. Corrisponde all'infrastruttura iniziale dello Sprint 1 del PRD.

| Step | Obiettivo | Deliverable | Dipendenze | Criterio di accettazione | Stato |
|---|---|---|---|---|---|
| 1.1 | Test baseline | Aggiungere `pytest`, `pytest-asyncio` e `httpx`; configurare raccolta test e fixture minime | Nessuna | `pytest` raccoglie ed esegue almeno un test verde | ✅ |
| 1.2 | Entry point API | Creare `backend/app/main.py` con app FastAPI e endpoint `/api/health` | 1.1 | `docker compose up --build` avvia il backend e `curl localhost:8000/api/health` restituisce HTTP 200 | ✅ |
| 1.3 | Migrazioni | Inizializzare Alembic in `backend/`, configurare ambiente async, `settings.database_url`, `Base.metadata` e import dei modelli | 1.2 | `alembic upgrade head` termina senza errori su un database vuoto | ✅ |

Il `Dockerfile` punta a `app.main:app` e il backend è verificabile sulla porta 8000. Il compose non monta il codice locale nel container: dopo modifiche a dipendenze o codice è necessario ricostruire l'immagine. Hardening Dockerfile, utente non-root e healthcheck di produzione sono rimandati alla fase opzionale finale.

## Fase 2 — Autenticazione

Questa fase completa la parte auth dello Sprint 1. Il modello `User` è stato confermato invariato; la fase è verificata con test API, service e persistenza.

| Step | Obiettivo | Deliverable | Dipendenze | Criterio di accettazione | Stato |
|---|---|---|---|---|---|
| 2.1 | Revisione User | Analizzare e confermare campi, vincoli, timestamp e responsabilità del modello | Gate esplicito dell'utente | Specifica approvata senza modificare il modello prima della conferma | ✅ |
| 2.2 | Persistenza User | Test di vincoli e CRUD; prima migrazione con tabella `users` | 1.3, 2.1 | Migrazione applicata; email unica e password memorizzata solo come hash | ✅ |
| 2.3 | Service auth | Registrazione, verifica password e login con `pwdlib`/Argon2 | 2.2 | Test unitari verdi per registrazione, credenziali valide e credenziali errate | ✅ |
| 2.4 | Router auth | Endpoint `/api/auth/register` e `/api/auth/login` con JWT | 2.3 | Test API verdi; login restituisce access token senza esporre la password | ✅ |
| 2.5 | Dipendenze auth | `get_current_user`, OAuth2 bearer e gestione degli errori 401 | 2.4 | Un endpoint protetto rifiuta token assente, invalido o scaduto | ✅ |

## Fase 3 — Spot e mappa

Questa fase implementa lo Sprint 2 del PRD.

| Step | Obiettivo | Deliverable | Dipendenze | Criterio di accettazione | Stato |
|---|---|---|---|---|---|
| 3.1 | Modello Spot | Modello con proprietario, nome, coordinate PostGIS POINT e raggio | Fase 2 | Test di validazione e persistenza dello spot verdi | ✅ |
| 3.2 | Migrazione Spot | Migrazione dello schema `spots` con indice spaziale se necessario | 3.1 | `alembic upgrade head` crea lo schema senza errori | ✅ |
| 3.3 | Service Spot | CRUD e query spaziali con controllo ownership | 3.2 | Un utente non può leggere o modificare spot di un altro utente | ⬜ |
| 3.4 | API Spot | Schemas Pydantic e router `/api/spots/*` | 3.3 | Test API verdi per creazione, lettura, modifica e cancellazione | ⬜ |
| 3.5 | Frontend base | Progetto React/Vite/Tailwind con autenticazione e client API | 3.4 | Frontend avviabile e login collegato al backend | ⬜ |
| 3.6 | Mappa | MapLibre con creazione, visualizzazione e selezione degli spot | 3.5 | L'utente vede e gestisce dalla mappa esclusivamente i propri spot | ⬜ |

## Fase 4 — Dati Open-Meteo

Questa fase implementa lo Sprint 3 del PRD.

| Step | Obiettivo | Deliverable | Dipendenze | Criterio di accettazione | Stato |
|---|---|---|---|---|---|
| 4.1 | Modello dati meteo | Tabelle per letture giornaliere e previsione associate a uno spot | Fase 3 | Test di persistenza e associazione allo spot verdi | ⬜ |
| 4.2 | Service meteo | Client `httpx` async per storico 14/30 giorni e previsione 7 giorni | 4.1 | Test con risposta Open-Meteo simulata e gestione del parsing verificata | ⬜ |
| 4.3 | Migrazione meteo | Migrazione delle tabelle e degli indici necessari | 4.1 | Schema aggiornato con Alembic senza perdita dei dati esistenti | ⬜ |
| 4.4 | Refresh API | Endpoint `/api/spots/{id}/refresh` con controllo ownership | 4.2, 4.3 | Un refresh salva dati per lo spot corretto e rifiuta spot non autorizzati | ⬜ |
| 4.5 | CLI meteo | Comandi `meteo fetch` e `meteo import` che riusano il service | 4.2 | CLI e API usano la stessa logica e producono risultati coerenti | ⬜ |

## Fase 5 — Dashboard MVP

Questa fase implementa lo Sprint 4 del PRD.

| Step | Obiettivo | Deliverable | Dipendenze | Criterio di accettazione | Stato |
|---|---|---|---|---|---|
| 5.1 | API dashboard | Endpoint per serie storiche, cumulati e previsioni dello spot | Fase 4 | Risposta validata con dati ordinati temporalmente | ⬜ |
| 5.2 | Grafici | Grafici Recharts per pioggia giornaliera e cumulata | 5.1 | L'utente vede andamento 14/30 giorni dello spot selezionato | ⬜ |
| 5.3 | Heatmap | Layer MapLibre per visualizzare l'intensità delle precipitazioni | 5.1 | La mappa mostra il layer meteo senza esporre dati di spot di altri utenti | ⬜ |
| 5.4 | Flusso MVP completo | Integrazione login, spot, refresh e dashboard | 5.2, 5.3 | Un utente registrato completa il percorso end-to-end senza interventi manuali sul DB | ⬜ |

## Fase 6 — Qualità e CLI finale

Questa fase chiude la MVP e consolida lo scheletro CLI esistente.

| Step | Obiettivo | Deliverable | Dipendenze | Criterio di accettazione | Stato |
|---|---|---|---|---|---|
| 6.1 | CLI DB | Collegare `db status`, `db migrate` e `db rollback` alle API Alembic | Fase 5 | I comandi riflettono e modificano lo stato reale delle migrazioni | ⬜ |
| 6.2 | Suite test | Test unitari service, test API e test di integrazione DB | Fasi 2-5 | Tutti i test passano in ambiente riproducibile | ⬜ |
| 6.3 | Qualità automatica | Configurare Ruff, type-check e pre-commit | 6.2 | Controlli automatici verdi su ogni modifica | ⬜ |
| 6.4 | Compose MVP | Aggiungere il servizio frontend e verificare lo stack completo | 5.4 | `docker compose up --build` avvia DB, backend e frontend | ⬜ |

## MVP completata quando

- un utente può registrarsi e autenticarsi;
- ogni utente può creare e gestire i propri spot GPS;
- l'app recupera storico e previsioni Open-Meteo per gli spot autorizzati;
- dashboard e mappa mostrano pioggia e previsioni;
- API, CLI e frontend condividono i service;
- migrazioni, test e controlli di qualità sono eseguibili in modo riproducibile;
- il flusso completo funziona con `docker compose up --build`.

## Fuori scope MVP

Notifiche, daily digest, weather alert, diario ritrovamenti, fenologia, correlazioni biologiche, sensori IoT e deploy VPS restano fasi successive.

## Note di contesto

- Il livello iniziale dell'utente richiede spiegazioni approfondite su PostgreSQL, SQLAlchemy e PostGIS.
- I trucchetti appresi vengono raccolti in `docs/project/tricks.md`.
- Documentazione e comunicazione del progetto sono in italiano; il codice non riceve commenti salvo richiesta esplicita.
- Lo stack MVP è FastAPI, SQLAlchemy async, GeoAlchemy2, Alembic, PostgreSQL/PostGIS, React/Vite/Tailwind, MapLibre, Recharts, Open-Meteo e Docker Compose.
