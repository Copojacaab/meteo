""" 
    conftest.py: 
        file speciale riconosciuto automaticamente da pytest che permette di definire strumenti condivisi da i test (fixture).
        Una fixture fornisce un contesto definito e affidabile per l'ambiente di test.

        Quando pytest vede test_settings(settings) in test_config.py, esegue prima la fixture, prende il valore restituito da Settings()
        e lo passa la test.
        Il vantaggio consiste nel separare la prepazione del test dal check vero e proprio: 
            Il test verifica il comportamento; la fixture prepara l'oggetto necessario

    Fixture DB (test di auth):
        clean_db   -> assicura che le tabelle esistano (create_all) e svuota users dopo ogni test
        db_session -> sessione AsyncSession collegata al DB di compose
        api_client -> client httpx che sovrascrive get_db, cosi' i test non dipendono dal wiring dell'app
"""
import pytest
import httpx
from sqlalchemy import delete


from app.config import Settings
from app.database import AsyncSessionLocal, Base, engine, get_db

from app.models.user import User
from app.models.spot import Spot


@pytest.fixture
def settings() -> Settings:
    return Settings()

@pytest.fixture
async def client():
    from app.main import app

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_db():
    # create_all e' idempotente: crea solo le tabelle mancanti
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with AsyncSessionLocal() as session:
        # ORDINE IMPORTANTE: Spot FK verso User (Referencial Integrity)
        await session.execute(delete(Spot))
        await session.execute(delete(User))
        await session.commit()


@pytest.fixture
async def db_session(clean_db):
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def api_client(clean_db):
    from app.main import app

    async def override_get_db():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
