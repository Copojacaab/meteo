"""
    __init__.py: 
        Import esplicito nel file di package init per rendere i modelli discoverable.
            Registrando i modelli in __init__.py, chiunque faccia 'from app.models import Base' attiva tutte le registrazioni. 
    
"""
from app.models.user import User
from app.models.spot import Spot

__all__ = ["User", "Spot"]

