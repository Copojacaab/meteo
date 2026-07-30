# Specifica di Progetto: Sistema di Tracking Meteo per Tartufai

## 1. Introduzione e Obiettivi

Il progetto nasce dall'esigenza dei cercatori di tartufi di monitorare i **microclimi** e l'**accumulo di pioggia** in aree geografiche circoscritte (spot di raccolta). I sistemi meteo tradizionali forniscono medie cittadine che non riflettono le condizioni reali dei boschi.

L'obiettivo è un'applicazione per il tracciamento delle precipitazioni, con predisposizione futura per dati biologici (fioritura) e sensori IoT, aiutando l'utente a identificare le condizioni ideali per la nascita dei tartufi preservando la segretezza degli spot.

## 2. Stack Tecnologico

| Componente | Scelta |
|---|---|
| **Backend** | FastAPI (Python) |
| **Frontend** | React + Vite + Tailwind CSS |
| **Mappa** | MapLibre GL JS |
| **Database** | PostgreSQL + PostGIS |
| **Meteo** | Open-Meteo API |
| **Auth** | JWT (access + refresh token) |
| **Deploy** | Docker Compose su VPS |

## 3. Architettura a Moduli

### Modulo 1: CORE — MVP (Fase 1)

Funzionalità minime per il funzionamento dell'app:

- **Autenticazione JWT:** Registrazione e login utente
- **Gestione Spot:** Interfaccia mappa (MapLibre) per salvare coordinate GPS con nome e raggio (es. 500m)
- **Integrazione Open-Meteo:** Recupero automatico di storico precipitazioni (14/30gg) e previsioni 7 giorni
- **Dashboard:** Grafici dell'andamento piogge per ogni spot + heatmap precipitazioni sulla mappa

### Modulo 2: NOTIFICHE & AUTOMAZIONE — Fase 2

- Schedulatore background per aggiornamento dati meteo
- Daily Digest (report serale/mattutino)
- Weather Alerter (avviso piogge non previste)

### Modulo 3: DIARIO & FENOLOGIA — Fase 2

- Quaderno dei ritrovamenti (data, spot, quantità, note)
- Taccuino fenologico (stato vegetativo piante simbionti)
- Motore di correlazione meteo + biologia + raccolti

### Modulo 4: IOT & SENSORISTICA — Futuro

- API ingestion per sensori fisici
- Pluviometro locale e sensore umidità terreno
- Data Override Logic (priorità a sensore fisico se online)

### Modulo 5: SICUREZZA — Trasversale

- Isolamento multi-tenancy (RLS PostgreSQL)
- JWT stateless

## 4. Roadmap

### Fase 1: MVP

| Sprint | Contenuto |
|---|---|
| **Sprint 1** | Docker Compose (Postgres/PostGIS + FastAPI + frontend), auth JWT, modello User |
| **Sprint 2** | Modello Spot (PostGIS), CRUD spot, mappa MapLibre |
| **Sprint 3** | Integrazione Open-Meteo API, cron job aggiornamento dati |
| **Sprint 4** | Dashboard con grafici (Chart.js/Recharts), heatmap precipitazioni |

### Fase 2: Evoluzione

- Notifiche (Daily Digest, Weather Alerter)
- Diario ritrovamenti e taccuino fenologico
- Motore di correlazione
- App mobile

### Fase 3: Futuro

- API IoT e integrazione sensori hardware
