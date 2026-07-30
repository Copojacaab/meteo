"""
    File di comandi per il database (migrate, rollback, status)
"""

import typer

db_app = typer.Typer(help="Comandi per la gestione del database")

@db_app.command()   # (a) 
def migrate(message: str):
    """Crea e applica una nuova migrazione"""
    pass

@db_app.command()
def rollback():
    """Annulla l'ultima migrazione"""
    pass

@db_app.command()
def status():
    """Mostra lo stato corrente delle migrazioni"""
    pass


# (a) registra la funzione come comando cli "CLI: meteo_cli migrate "add spots table" "
                            #  Typer: vede che db é sottogruppo -> carica db_app
                            #           vede che migrate é un comando -> chiama la funzione migrate()
                            #           passa "add spots table" come parametro message