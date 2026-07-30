"""
    Entry point principale (crea l'app Typer per interfacciarci con la CLI usanto type hints)
"""

import typer

# (1) App principale CLI
app = typer.Typer(help="Meteo CLI")

# (2) Registrazione sottogruppi di comandi
from .db_commands import db_app
from .meteo_commands import meteo_app

app.add_typer(db_app, name="db")
app.add_typer(meteo_app, name="meteo")

if __name__ == "__main__":
    app()