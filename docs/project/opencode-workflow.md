# Workflow manuale OpenCode

## Scopo

Questo documento definisce due modalità alternative per usare OpenCode come consulente di sviluppo. In entrambi i casi la scrittura del codice resta principalmente a carico dello sviluppatore: OpenCode analizza, intervista, propone, verifica e segnala il prossimo passaggio.

I due workflow sono applicabili a due livelli:

- **macro-progetto**: obiettivi, requisiti, architettura e suddivisione sistemica;
- **singolo componente**: progettazione e realizzazione di una parte delimitata del sistema.

Il passaggio da un agente al successivo è sempre manuale. L’agente corrente conclude il proprio lavoro, produce l’artefatto previsto e indica quale agente dovrebbe essere attivato dopo.

## Regole comuni

### Autonomia

| Attività | Regola |
|---|---|
| Analisi del repository | OpenCode può procedere direttamente. |
| Test e comandi di verifica | OpenCode può eseguirli direttamente e riportare i risultati. |
| Aggiornamento di documentazione già esistente | Diretto, ma solo dopo un’intervista approfondita e adattiva. |
| Modifica di configurazioni e piani | Diretta. |
| Scrittura o modifica del codice | OpenCode prepara una proposta breve; l’applicazione richiede approvazione esplicita. |
| Creazione di un nuovo file documentale | Proposta al termine del passaggio, prima della creazione. |

Una proposta per un nuovo file deve spiegare:

1. cosa descriverebbe;
2. quanto è necessario;
3. perché non è sufficiente aggiornare un artefatto esistente.

### User interview

L’intervista precede ogni aggiornamento di un artefatto corrente. La profondità è adattiva: aumenta quando crescono ambiguità, rischio, impatto architetturale o numero di dipendenze; resta breve per decisioni locali e ben definite.

L’intervista termina soltanto quando l’agente presenta un riepilogo e lo sviluppatore lo conferma esplicitamente. Il riepilogo deve rendere chiari, quando pertinenti:

- obiettivo;
- vincoli e assunzioni;
- risultato atteso;
- elementi fuori scope;
- dubbi ancora aperti.

Senza conferma, l’agente non crea né aggiorna l’artefatto ufficiale.

### Artefatti globali

Gli artefatti sono globali e contengono sottosezioni dedicate ai componenti. Non si crea una struttura separata per ogni componente.

```text
artefacts/
├── requisiti/
│   ├── _current.md
│   └── all_version/
├── architettura/
│   ├── _current.md
│   └── all_version/
├── specifiche/
│   ├── _current.md
│   └── all_version/
└── decisioni/
    ├── _current.md
    └── all_version/
```

Gli artefatti per i componenti sono sezioni interne ai file correnti, per esempio `specifiche/_current.md > Componente: autenticazione`.

Ogni categoria segue queste regole:

- `_current.md` contiene lo stato ufficiale corrente e la cronologia interna delle versioni;
- `all_version/` conserva tutti i file prodotti, senza cancellazioni;
- le versioni sono numeriche (`v001`, `v002`, ...);
- ogni versione riporta nel documento la data di produzione o aggiornamento;
- ogni artefatto riporta uno stato esplicito, ad esempio `draft`, `in_review`, `approved` o `superseded`;
- prima di aggiornare `_current.md` si conduce una nuova breve intervista;
- un conflitto con un artefatto precedente blocca il passaggio: l’agente descrive il conflitto e chiede una decisione.

Un file di versione può avere un nome come `v003.md` e iniziare così:

```markdown
# Requisiti — v003

- Data: 2026-08-05
- Stato: approved
- Sostituisce: v002
```

### Handoff

L’handoff è volutamente sintetico. Contiene soltanto:

- artefatto prodotto o aggiornato;
- risultato del passaggio;
- questioni aperte, se presenti;
- prossimo agente suggerito.

Il contenuto completo resta nell’artefatto, non viene duplicato nell’handoff.

### Coerenza con il progetto globale

Durante il lavoro su un componente, l’agente verifica gli artefatti globali quando il componente tocca:

- architettura;
- requisiti;
- decisioni condivise.

Per dettagli locali e isolati non è necessaria una verifica globale aggiuntiva.

### Codice e test

L’agente di consulenza all’implementazione può essere attivato durante la scrittura per rispondere a dubbi puntuali. Può produrre pseudocodice, esempi o una patch breve, ma la patch richiede sempre approvazione prima di essere applicata.

Una proposta di codice contiene solo il necessario:

- cosa cambiare;
- dove cambiare;
- comportamento atteso;
- verifica suggerita.

Se un test fallisce, l’agente analizza il fallimento e propone una diagnosi. Non modifica il codice senza approvazione.

---

# Workflow A — Agenti specializzati

## Idea

Ogni fase ha un agente dedicato, un obiettivo delimitato e un artefatto di uscita. Gli agenti hanno un ruolo principale preciso, ma possono segnalare problemi appartenenti a fasi precedenti.

Il vantaggio è la separazione netta delle responsabilità. Il costo è un numero maggiore di switch manuali.

## Agenti

| Agente | Responsabilità principale | Artefatto di uscita |
|---|---|---|
| Intervistatore | Chiarire obiettivo, contesto, vincoli e risultato atteso | Sezione di intervista in `requisiti` |
| Analista requisiti | Trasformare il contesto confermato in requisiti | `requisiti` |
| Architetto sistemico | Definire confini, dipendenze e flussi globali | `architettura` |
| Analista decisioni | Esplicitare scelte, alternative e motivazioni | `decisioni` |
| Progettista componenti | Proporre la scomposizione del progetto o la struttura del componente | `specifiche` |
| Consulente implementazione | Supportare la scrittura manuale del codice | Nota breve in `specifiche` o aggiornamento richiesto |
| Revisore | Confrontare codice, test e artefatti rilevanti | Esito in `decisioni` |
| Consolidatore | Condurre l’intervista finale e aggiornare gli artefatti correnti | `_current.md` nelle categorie coinvolte |

Il Consulente implementazione non è un agente di implementazione automatica. Il suo compito è rispondere a domande, proporre soluzioni e preparare patch soggette ad approvazione.

## Passaggi del macro-progetto

### A1 — Intervista iniziale - Metis

L’Intervistatore conduce un’intervista adattiva sul progetto. Non decide l’architettura e non trasforma autonomamente ipotesi in requisiti approvati.

**Output:** un file di versione nella sezione progetto di `requisiti`, con riepilogo confermato, domande aperte e prossimo agente suggerito: Analista requisiti.

### A2 — Requisiti - Prometheus

L’Analista requisiti usa il riepilogo confermato per definire obiettivi, requisiti, vincoli, fuori scope e criteri di accettazione. Se emergono ambiguità, torna all’Intervistatore invece di risolverle per supposizione.

**Output:** versione di `requisiti` con stato `in_review` o `approved`, in base alla conferma ricevuta.

### A3 — Architettura sistemica - Oracle

L’Architetto sistemico definisce componenti, responsabilità, interfacce, flussi, dipendenze e punti di integrazione. Deve consultare il codice e la documentazione tecnica esistente prima di proporre cambiamenti incompatibili.

**Output:** versione di `architettura` e lista sintetica delle decisioni che richiedono l’Analista decisioni.

### A4 — Decisioni e motivazioni - Oracle

L’Analista decisioni raccoglie le scelte architetturali e tecniche, le alternative considerate e le motivazioni. Un’alternativa non sufficientemente valutata resta una proposta aperta, non una decisione.

**Output:** versione di `decisioni` con decisioni confermate e proposte aperte.

### A5 — Scomposizione e specifiche - Prometheus

Il Progettista componenti propone la suddivisione in componenti oppure, se il componente è già noto, ne definisce responsabilità, contratti, dati, flussi e criteri di completamento.

**Output:** versione di `specifiche` con sottosezioni per i componenti coinvolti.

### A6 — Implementazione manuale assistita - Sysyphus (eventuale supporto librarian)

Lo sviluppatore scrive il codice. Il Consulente implementazione viene attivato manualmente per dubbi puntuali, scelte locali o proposte di patch.

**Output:** nota di implementazione o aggiornamento richiesto nella specifica del componente. Il codice viene modificato solo dopo approvazione esplicita.

### A7 — Revisione - Oracle(o skill review-work)

Il Revisore verifica il codice e i test rispetto alle specifiche e controlla la coerenza con gli artefatti globali rilevanti. Segnala problemi di implementazione, test mancanti, regressioni e conflitti documentali.

**Output:** esito di revisione in `decisioni`, con esito, problemi aperti e prossimo agente suggerito.

### A8 — Consolidamento - Sisyphus

Il Consolidatore conduce una nuova breve intervista sulla modifica effettivamente realizzata. Dopo la conferma, aggiorna direttamente gli `_current.md` coinvolti e archivia le nuove versioni in `all_version/`.

**Output:** artefatti correnti aggiornati e ciclo chiuso oppure nuovo passaggio indicato se restano problemi.

## Diagramma macro-progetto

```text
[Intervistatore]
       |
       v
[Analista requisiti] --> requisiti/vNNN.md
       |
       v
[Architetto sistemico] --> architettura/vNNN.md
       |
       v
[Analista decisioni] --> decisioni/vNNN.md
       |
       v
[Progettista componenti] --> specifiche/vNNN.md
       |
       v
[Implementazione manuale]
       |
       v
[Consulente implementazione]
       |
       v
[Revisore] --> esito in decisioni/vNNN.md
       |
       v
[Consolidatore + nuova intervista]
       |
       v
[_current.md aggiornati]
```

Ogni rettangolo rappresenta un’attivazione manuale. Dopo ogni passaggio l’agente comunica il prossimo agente suggerito; non lo attiva autonomamente.

## Passaggi del singolo componente

Il ciclo del componente è una versione ridotta del ciclo macro, ma mantiene gli stessi controlli.

```text
[Intervistatore componente]
       |
       v
[Progettista componente] --> specifiche/vNNN.md
       |
       v
[Verifica coerenza globale, se necessaria]
       |
       v
[Implementazione manuale + Consulente implementazione]
       |
       v
[Revisore] --> esito in decisioni/vNNN.md
       |
       v
[Consolidatore + nuova breve intervista]
       |
       v
[_current.md aggiornati]
```

Se durante il ciclo emergono cambiamenti a requisiti, architettura o decisioni condivise, il ciclo del componente si interrompe e segnala il ritorno all’agente specializzato corrispondente.

---

# Workflow B — Agenti generalisti

## Idea

Pochi agenti generalisti vengono attivati in fasi diverse. La distinzione non è data da un agente per ogni micro-fase, ma dal mandato esplicito assegnato nell’attivazione e dall’artefatto richiesto.

Il vantaggio è un numero inferiore di switch e una maggiore continuità di contesto. Il rischio è che un agente allarghi il proprio ruolo: il mandato e l’artefatto di uscita devono quindi restare espliciti.

## Agenti

| Agente | Responsabilità principale | Mandati possibili |
|---|---|---|
| Consulente di progetto | Intervistare, chiarire e strutturare il problema | Intervista, requisiti, scomposizione componenti |
| Consulente tecnico | Analizzare il repository e progettare soluzioni | Architettura, specifiche, decisioni, supporto implementazione |
| Revisore/verificatore | Verificare risultati e proporre il consolidamento | Revisione codice, test, coerenza globale, chiusura |

Un agente generalista non può assumere un mandato diverso da quello indicato. Per esempio, il Consulente tecnico in mandato “specifica componente” non decide autonomamente di riscrivere l’architettura.

## Passaggi del macro-progetto

### B1 — Consulente di progetto: intervista e requisiti

Il Consulente di progetto conduce l’intervista adattiva. Dopo la conferma, produce il riepilogo e l’artefatto requisiti. Se la scomposizione in componenti è già possibile senza nuove decisioni architetturali, può includere una proposta iniziale; altrimenti la lascia come domanda aperta.

**Output:** versione di `requisiti` e prossimo mandato: Consulente tecnico / architettura.

### B2 — Consulente tecnico: architettura

Con mandato “architettura”, il Consulente tecnico analizza gli artefatti correnti e il repository, quindi definisce struttura, flussi, dipendenze e punti di integrazione.

**Output:** versione di `architettura` e decisioni da confermare in `decisioni`.

### B3 — Consulente tecnico: decisioni e specifiche

Con mandato “decisioni”, esplicita alternative e motivazioni. Con mandato “specifica componente”, definisce il componente, i suoi contratti e i criteri di completamento. Sono due attivazioni distinte anche se svolte dallo stesso agente.

**Output:** versione di `decisioni` oppure `specifiche`, mai entrambi senza dichiarare chiaramente i due risultati.

### B4 — Consulente tecnico: supporto all’implementazione

Con mandato “supporto implementazione”, risponde ai dubbi dello sviluppatore e può proporre una patch breve. Non applica codice e non modifica gli artefatti ufficiali senza rispettare l’intervista e la conferma previste.

**Output:** nota breve collegata alla specifica del componente oppure proposta di patch da approvare.

### B5 — Revisore/verificatore: revisione

Il Revisore/verificatore controlla codice, test e coerenza con gli artefatti globali rilevanti. Se trova un conflitto, si ferma e lo espone; non lo risolve per conto proprio.

**Output:** esito di revisione in `decisioni` e prossimo mandato suggerito.

### B6 — Consulente di progetto o Revisore/verificatore: consolidamento

Il consolidamento richiede una nuova breve intervista. In base al mandato scelto, il Consulente di progetto o il Revisore/verificatore aggiorna gli `_current.md` direttamente dopo la conferma.

**Output:** versioni archiviate in `all_version/`, `_current.md` aggiornati e stato finale del lavoro.

## Diagramma macro-progetto

```text
[Consulente di progetto]
  mandato: intervista + requisiti
       |
       v
requisiti/vNNN.md
       |
       v
[Consulente tecnico]
  mandato: architettura
       |
       v
architettura/vNNN.md
       |
       v
[Consulente tecnico]
  mandato: decisioni + specifiche
       |
       v
decisioni/vNNN.md + specifiche/vNNN.md
       |
       v
[Implementazione manuale]
  mandato eventuale: supporto implementazione
       |
       v
[Revisore/verificatore]
  mandato: revisione
       |
       v
[Consolidamento dopo nuova intervista]
       |
       v
[_current.md aggiornati]
```

## Passaggi del singolo componente

```text
[Consulente di progetto]
  mandato: intervista componente
       |
       v
[Consulente tecnico]
  mandato: specifica componente
       |
       v
specifiche/vNNN.md
       |
       v
[Consulente tecnico]
  mandato eventuale: verifica coerenza globale
       |
       v
[Implementazione manuale]
       |
       v
[Revisore/verificatore]
  mandato: revisione componente
       |
       v
[Consolidamento dopo nuova intervista]
       |
       v
[_current.md aggiornati]
```

Se il componente modifica requisiti, architettura o decisioni condivise, il Revisore/verificatore segnala il ritorno al mandato globale appropriato del Consulente di progetto o del Consulente tecnico.

---

# Regole di scelta

## Quando usare Workflow A

Usare gli agenti specializzati quando:

- il progetto è nuovo o sta cambiando direzione;
- le decisioni architetturali sono numerose o rischiose;
- serve una separazione forte tra requisiti, architettura e revisione;
- si vuole massimizzare la tracciabilità dei passaggi.

## Quando usare Workflow B

Usare gli agenti generalisti quando:

- il contesto è già stabile e documentato;
- il componente è ben delimitato;
- si vuole ridurre il numero di switch;
- la continuità di contesto è più importante della separazione massima dei ruoli.

I due workflow possono essere usati nello stesso progetto, ma la scelta deve essere esplicita per il ciclo in corso. Un passaggio da A a B, o viceversa, va registrato in `decisioni` se modifica il modo in cui vengono prodotti o approvati gli artefatti.

## Stato minimo di un passaggio

Un passaggio è concluso solo quando:

1. l’intervista richiesta è stata completata;
2. il riepilogo è stato confermato, quando previsto;
3. l’artefatto è stato prodotto o la proposta di nuovo file è stata presentata;
4. eventuali conflitti sono stati fermati e segnalati;
5. l’handoff sintetico indica il prossimo agente o mandato;
6. il codice, se coinvolto, è stato soltanto proposto e non applicato senza approvazione.

## Comandi manuali concettuali

I nomi seguenti descrivono lo switch, non impongono ancora una configurazione specifica di OpenCode:

```text
attiva intervistatore --scope progetto
attiva analista-requisiti --artefatto requisiti
attiva architetto-sistemico --artefatto architettura
attiva analista-decisioni --artefatto decisioni
attiva progettista-componenti --componente <nome>
attiva consulente-implementazione --componente <nome>
attiva revisore --componente <nome>
attiva consolidatore --artefatti <categorie>
```

Nel Workflow B i comandi indicano il mandato dell’agente:

```text
attiva consulente-progetto --mandato intervista-requisiti
attiva consulente-tecnico --mandato architettura
attiva consulente-tecnico --mandato specifica --componente <nome>
attiva consulente-tecnico --mandato supporto-implementazione
attiva revisore-verificatore --mandato revisione --componente <nome>
```

Questi comandi sono una convenzione operativa da trasformare, in un secondo momento, nella configurazione concreta degli agenti e dei prompt di OpenCode.
