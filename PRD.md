# Product Requirements Document (PRD)

# Specifica di Progetto: Sistema di Tracking Meteo e Fenologico per Tartufai

## 1. Introduzione e Obiettivi

Il progetto nasce dall'esigenza specifica dei cercatori di tartufi di monitorare i **microclimi** e l'**accumulo millimetrico di pioggia** in aree geografiche circoscritte (spot di raccolta). I sistemi meteo tradizionali forniscono medie cittadine che non riflettono le reali condizioni dei boschi o delle zone montuose.

L'obiettivo è creare un'applicazione che consenta il tracciamento a lungo termine delle precipitazioni, l'integrazione di dati biologici (fioritura delle piante) e la predisposizione per sensori IoT sul campo, aiutando l'utente a identificare le condizioni perfette per la nascita dei tartufi preservando la totale segretezza dei propri spot.

---

## 2. Architettura Funzionale (I 5 Moduli)

### Modulo 1: CORE (Il Motore di Base)

Garantisce le funzionalità minime per il funzionamento dell'applicazione (MVP).

- **Gestione Spot (Geofencing base):** Interfaccia mappa in cui l'utente può salvare coordinate GPS precise assegnando un nome e un raggio di interesse (es. 500 metri).
- **Integrazione Provider Meteo (Open-Meteo):** Interfacciamento con le API esterne di Open-Meteo per scaricare in modo automatizzato:
  - Lo storico delle precipitazioni (es. cumulato degli ultimi 14 e 30 giorni).
  - Previsioni orarie e giornaliere per i successivi 7 giorni.
- **Dashboard di Visualizzazione:** Schermata principale (inizialmente Web Responsive) con grafici chiari e intuitivi sull'andamento delle piogge per ciascuno spot salvato.

### Modulo 2: NOTIFICHE & AUTOMAZIONE (La Proattività)

Evita all'utente di dover controllare manualmente l'applicazione, spingendo le informazioni rilevanti al momento giusto.

- **Schedulatore di Background (Cron Jobs):** Processo lato server per l'aggiornamento automatico dei dati meteo a orari prestabiliti.
- **Daily Digest (Riepilogo Programmato):** \* _Sera (20:00 - 21:00):_ Bilancio della giornata (es. millimetri caduti, trend umidità) per pianificare le uscite del giorno successivo.
  - _Mattina (07:00):_ Focus sulle previsioni della giornata e sull'accumulo notturno.
- **Weather Alerter:** Sistema di monitoraggio che invia un avviso immediato se i radar meteo rilevano precipitazioni intense non previste o superiori a una determinata soglia in uno degli spot salvati.

### Modulo 3: DIARIO & FENOLOGIA (Il Cervello Analytics)

Trasforma i dati grezzi in insight predittivi legando il meteo alla botanica e alla raccolta reale.

- **Quaderno dei Ritrovamenti:** Registro privato dove l'utente inserisce i dati delle raccolte (Data, Spot, Quantità, Qualità/Specie di tartufo, Note).
- **Registro della Fioritura (Taccuino Fenologico):** Annotazione dello stato vegetativo delle "piante spia" o simbionti (es. Quercia, Nocciolo, Biancospino) con relativi stadi (Gemma, Piena fioritura, Caduta foglie). X
- **Il Triangolo dei Dati (Motore di Correlazione):** Algoritmo che incrocia automaticamente:
  1.  _Dati Meteo/IoT:_ Pioggia e umidità accumulate nei 14-30 giorni precedenti.
  2.  _Dati Biologici:_ Stato della fioritura/fenologia nello spot.
  3.  _Output:_ Successo della raccolta per identificare i pattern ideali di nascita.

### Modulo 4: IOT & SENSORISTICA (L'Evoluzione Hardware)

Predisposizione per superare l'approssimazione dei modelli meteo teorici tramite hardware sul campo.

- **Ingestion API:** Endpoint protetti e ottimizzati per ricevere pacchetti dati trasmessi da centraline nascoste nei boschi.
- **Sensori Target:** Pluviometro locale (sotto chioma) e sensore di umidità del terreno a livello delle radici.
- **Data Override Logic:** Algoritmo che assegna priorità al dato fisico del sensore se aggiornato nelle ultime 24 ore, effettuando il fallback sul dato stimato di Open-Meteo in caso di sensore offline.

### Modulo 5: SECURITY & PRIVACY (La Fondazione)

Strato trasversale per proteggere il segreto industriale di ogni tartufaio.

- **Isolamento degli Spot (Multi-tenancy rigida):** Struttura del database progettata affinché nessun utente possa intercettare o visualizzare le coordinate geografiche degli spot altrui.
- **Autenticazione Stateless (JWT):** Token di sicurezza ideali sia per l'architettura Web iniziale che per il futuro passaggio ad app mobile nativa.

---

## 3. Strategia di Sviluppo e Stack Tecnologico

L'approccio scelto è **API-First** per garantire massima flessibilità e velocità di sviluppo (Fast Developing).

- **Backend:** Sviluppo di un'API REST indipendente utilizzando framework performanti e snelli come **FastAPI (Python)** o **Node.js**. Questo permetterà di mantenere lo stesso identico motore di backend sia per la Web App che per la futura App Mobile.
- **Frontend Web:** Single Page Application (SPA) responsive ottimizzata per l'uso da smartphone tramite utility come **Tailwind CSS**.
- **Database:** **PostgreSQL** con estensione spaziale **PostGIS** per gestire in modo ottimale le coordinate geografiche, il geofencing e le serie temporali delle precipitazioni.
- **Sorgente Dati Meteo:** **Open-Meteo API** (gratuita per uso non commerciale, senza necessità iniziale di API Key, basata su modelli storici accurati come ERA5).
- **Hosting e Deployment:** Hosting su una **VPS** (es. Hetzner, DigitalOcean, OVH) gestito tramite **Docker e Docker Compose** per isolare i servizi (Backend, Database, Nginx come reverse proxy e Let's Encrypt per la gestione automatica del certificato SSL/HTTPS).

---

## 4. Roadmap di Rilascio (Fasi del Progetto)

| Fase 1: MVP (Web App V1)                             | Fase 2: Evoluzione (App Mobile & IoT)              |
| :--------------------------------------------------- | :------------------------------------------------- |
| Registrazione utenti e autenticazione JWT            | Sistema di Notifiche Push (Daily Digest & Alerter) |
| Gestione Spot su Mappa (Core Geofencing)             | Taccuino Fenologico (Fioriture delle piante)       |
| Integrazione dati Storici/Previsioni Open-Meteo      | Algoritmo di Correlazione (Triangolo dei Dati)     |
| Dashboard responsive con grafici pioggia 14/30gg     | Ingestion API e Integrazione Sensori Fisici (IoT)  |
| Isolamento e crittografia lato DB degli spot salvati | Sviluppo App Mobile Nativa (iOS / Android)         |

specifiche_progetto_meteo_tartufai.md
Visualizzazione di specifiche_progetto_meteo_tartufai.md.
