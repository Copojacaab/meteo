Fase 0: "Prompt Buddy": Inizia chiedendo a Gemini: "Voglio avviare un nuovo progetto. Facciamo un brainstorming strutturato. Inizia ponendomi 5 domande mirate per definire l'obiettivo, i vincoli e lo stack tecnologico che ho in mente."

    ## Core:
        L'applicazione deve ruotare intorno al concetto di "zona di monitoraggio":
            - **geofencing**: l'utente non cerca una cittá, salva un punto sulla mappa (coordinate GPS o magari touch con una mappa) con un determinato raggio di interesse (o magari anche definibile a forma) (ad esempio un bosco specifico)
            - **aggregazione delle precipitazioni**: dashboard con metriche tipo: "nello spot A sno caduti 12 mm di pioggia nelle ultime 48 ore e 45 mm negli ultimi 15 giorni"(o comunque lasso temporale di interesse definibile per zone). Questo indica se il terreno ha un umiditá giusta.
            - **previsioni mirate**: un trend delle precipitazioni previste nelle settimane successive
            - **integrazione provider meteo**: open-meteo
    ### Notifiche e Automazione
        Elabora i dati in background e fa user push:
            - **schedulatore in background**: fa polling a orari fissi dei dati meteo (open-meteo)
            - **daily digest**: generatore di report serale o mattutino con il riassunto dello stato degli spot
            - **weather  alerter**: sistema che confronta le previsioni precedenti con il meteo effettivo in tempo reale e triggera un avviso se rileva piogge non programmate
    ### Diario e Analytics
        - **notebook dei ritrovamenti**: input di dati da parte dell'utente (data, spot, quantitá/qualitá, note e foto)
        - **notebook fioritura: l'utente puó annotare lo stato vegetativo delle piante in uno specifico spot:
            - input: tipo di pianta, stato (inizio, fioritura,caduta e che cazzo ne so) e data osservazione
        - **correlation engine**: logica software (qualcosa mi invento) che incrocia:
            1. Dato meteo: quanta pioggia é caduta
            2. Dato biologico: stato fioritura/piante
            3. Dato di output: qualitá e quantitá tartufi trovati
        - **magari anche uno storico dei cani**

    ### IOT
        *Future proof*
        - **Ingestion API**: endpoint protetti e ultra-leggeri dove gateway e nodi IoT inviano i pacchetti dati (umiditá terreno%, pluvimetro locale mm)
    ### SECURITY & PRIVACY
        - Autenticazione stateless (JWT): gestione login e mantenimento della sessione sia per web app che per mobile

    Funzione tipo: inizia la raccolta (nike running). Tramite gps ti segue, ti dice dove sei stato, puoi segnare i punti di raccolta con precisione GPS...


    ## CORE 2
        Visualizzazione grafica di una mappa che si colora dinamicamente in base all'accumulo di pioggia nel periodo selezionato dall'utente.
        - **mappatura del territorio**(grid mesh): mappa il territorio dividendolo in celle (quadrate o a nido per il gradiente). Ogni quadrato interroga il backend per sapere quanta pioggia ha accumulato (meccanismo subscriber/publisher)
        - **mappa delle anomalie**:0% pioggia identica alla media storica -> grigio neutro; -30% -> sfumature giallo/arancione; +30% -> sfumature azzurro/blu.
        - **preset temporali**:
            - *per settimana*: < 5mm -> grigio, 5-15mm -> azzurro, ...
            - *per mese*: <15mm -> grigio, 15-40mm-> azzurro..
            - *ultimi sei mesi*:...
            - *ultimo anno*:...
    ### Modalitá Focus
        Quando l'utente clicca su una zona della mappa, l'applicazione attiva la focus mode:
        - **zoom automatico**: la mappa zooma sull'area circoscritta passando dalla visualizzazione macro a quella topografica
        - **pannello laterale slide over**: si apre un pannello con i dati specifici di quel punto:
            - grafico delle precipitazioni giorno per giorno del mese passato
            - temperatura media
            - data ultima pioggia significativa
        - **crea spot segreto**: pulsante che permette di convertire quell'area di focus in "spot da controllare" del modulo Core 1, iniziando a monitorarla permanentemente in dashboard

Fase 1: "Plan Mode": Una volta definita l'idea, passa alla modalità pianificazione. Chiedi: "Crea una roadmap per questo progetto, dividendo il lavoro in fasi (Ricerca, Design, Prototipazione, Test)".

Fase 2: "Sfidare le assunzioni": Usa il modello per fare l'avvocato del diavolo: "Quali sono i 3 punti di fallimento più probabili in questa architettura considerando l'uso di [tecnologia scelta]?".

Fase 3: "Visualizzazione": Chiedi di generare diagrammi Mermaid per visualizzare il flusso dei dati o la struttura del database.
