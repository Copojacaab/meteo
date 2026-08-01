# Quaderno dei Trucchetti — Meteo Tartufai

> Raccoglie i trucchetti di programmazione appresi durante lo sviluppo.
> Scopo: ripeterli, ricordarli, capirli in contesti diversi.
> Aggiungi un trucchetto a ogni step completato.

## Trucchetti raccolti

### 1. `yield` vs `return` (generator)
- `yield`: restituisce un valore **e mette in pausa** la funzione. Alla chiamata successiva riprende da dove era stata interrotta.
- `return`: termina la funzione e restituisce un valore.
- Uso in FastAPI: `get_db()` è un generator che la dependency usa per iniettare la sessione per richiesta; il `with` garantisce la chiusura.

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # pausa qui, FastAPI usa session, poi chiude
```

### 2. `echo=True` nell'engine SQLAlchemy
- Stampa su console **ogni query SQL inviata** al database.
- Vedi le **domande**, non le risposte (quelle tornano nel codice Python).
- Serve per debug; in produzione va rimosso (spam nei log).

```python
engine = create_async_engine(DATABASE_URL, echo=True)
```

### 3. Esplorare funzioni di libreria con stdlib
Quando una libreria è mal documentata, il Python standard basta:

```bash
python -c "from modulo import funzione; help(funzione)"        # docstring + firma
python -c "import inspect; from modulo import funzione; print(inspect.signature(funzione))"  # parametri
python -c "import inspect; from modulo import funzione; print(inspect.getsource(funzione))"   # sorgente!
```

- `inspect.getsource()` è la chiave maestra: legge l'implementazione reale.
- Anche `print(funzione.__doc__)` funziona.

### 4. Import relativi con `.`
- `from .db_commands import db_app` = "dalla stessa cartella".
- Senza il `.`, Python cerca nel filesystem globale, non nel package corrente.

### 5. Decoratori per registrare comandi (Typer)
- `@db_app.command()` registra la funzione come comando CLI.
- `app.add_typer(db_app, name="db")` registra un sottogruppo.
- Typer genera automaticamente `--help` da docstring e type hints.

### 6. Docstring sincrona per funzioni async
- Se una funzione async è "mostly identical" alla versione sincrona, la docstring dettagliata sta in quella sincrona.
- Esempio: `create_async_engine` → leggere `create_engine` per `pool_size`, `max_overflow`, ecc.

### 7. Connection pool SQLAlchemy
- `pool_size` (default 5): connessioni **permanenti** tenute aperte e riutilizzate.
- `max_overflow` (default 10): connessioni **temporanee** di emergenza, chiuse appena rilasciate.
- Massimo totale simultaneo = pool_size + max_overflow (15).
- Connessioni pool = riutilizzate; overflow = si aprono quando il pool è saturo e si chiudono subito dopo.

## Regole d'uso

- Aggiungi UN trucchetto per step, con esempio minimo.
- Se un trucchetto è già presente, non duplicarlo: aggiungi il nuovo contesto d'uso.
