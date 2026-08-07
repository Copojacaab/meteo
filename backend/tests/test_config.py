async def test_settings(settings):                  # settings e' la fixture definita in conftest.py
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.secret_key != "" 
