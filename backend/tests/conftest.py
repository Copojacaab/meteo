""" 
    conftest.py: 
        file speciale riconosciuto automaticamente da pytest che permette di definire strumenti condivisi da i test (fixture).
        Una fixture fornisce un contesto definito e affidabile per l'ambiente di test.

        Quando pytest vede test_settings(settings) in test_config.py, esegue prima la fixture, prende il valore restituito da Settings()
        e lo passa la test.
        Il vantaggio consiste nel separare la prepazione del test dal check vero e proprio: 
            Il test verifica il comportamento; la fixture prepara l'oggetto necessario
"""

import pytest
import httpx
from app.config import Settings

@pytest.fixture
def settings() -> Settings:
    return Settings()

@pytest.fixture
async def client():
    from app.main import app

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

