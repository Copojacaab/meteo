"""
    database.py: 

    Cosa fa: 
        Crea l'infrastruttura di connessione al database PostgreSQL 
        Senza engine e sessioni, nessun modello puó leggere o scrivere dati. É il layer piú basso su cui ci appoggiano  
            models -> services -> routers
    
    Come: 
        1. Crea pool di connessioni (engine)
        2. Espone un factory di sessioni
        3. Espone la Base che erediteranno tutti i modelli (models)
        4. Espone il generatore (get_db()) che FastApPI userá come dependency per iniettare la sessione in ogni endpoint
"""

# === My import ===
from .config import settings
# =================

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = settings.database_url

#  (1) crea engine asincrono
engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

# (2) crea la factory di sessioni
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# (3) crea la Base class per i modelli
class Base(AsyncAttrs, DeclarativeBase):
    pass

# (4) dependency per fasAPI: yield alla sessione
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
