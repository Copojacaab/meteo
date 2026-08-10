"""
    Step 2.4 / 2.5 — API auth:
    register/login con JWT senza esporre la password, endpoint protetto /me,
    rifiuto di token assente, invalido e scaduto.
"""
from datetime import timedelta

import httpx
from sqlalchemy import delete

from app.database import AsyncSessionLocal
from app.models.user import User
from app.services.auth import create_access_token

USER = {"email": "user@example.com", "password": "secret123"}


async def register(client: httpx.AsyncClient) -> httpx.Response:
    return await client.post("/api/auth/register", json=USER)


async def login(client: httpx.AsyncClient, email: str = USER["email"], password: str = USER["password"]) -> httpx.Response:
    return await client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
    )


async def test_register_returns_user_without_password(api_client):
    response = await register(api_client)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == USER["email"]
    assert "id" in body
    assert "created_at" in body
    assert "password" not in body
    assert "hashed_password" not in body


async def test_register_duplicate_email_returns_409(api_client):
    await register(api_client)

    response = await register(api_client)

    assert response.status_code == 409


async def test_register_invalid_email_returns_422(api_client):
    response = await api_client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "secret123"},
    )

    assert response.status_code == 422


async def test_login_with_valid_credentials_returns_token(api_client):
    await register(api_client)

    response = await login(api_client)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert USER["password"] not in response.text


async def test_login_with_wrong_password_returns_401(api_client):
    await register(api_client)

    response = await login(api_client, password="wrong-password")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_login_with_unknown_email_returns_401(api_client):
    response = await login(api_client, email="ghost@example.com")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_me_returns_current_user(api_client):
    await register(api_client)
    token = (await login(api_client)).json()["access_token"]

    response = await api_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == USER["email"]
    assert "hashed_password" not in body


async def test_me_without_token_returns_401(api_client):
    response = await api_client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_me_with_invalid_token_returns_401(api_client):
    response = await api_client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-valid-token"})

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_me_with_expired_token_returns_401(api_client):
    registered = await register(api_client)
    user_id = registered.json()["id"]
    expired_token = create_access_token(user_id, expires_delta=timedelta(minutes=-5))

    response = await api_client.get("/api/auth/me", headers={"Authorization": f"Bearer {expired_token}"})

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_me_with_token_of_deleted_user_returns_401(api_client):
    registered = await register(api_client)
    token = (await login(api_client)).json()["access_token"]

    async with AsyncSessionLocal() as session:
        await session.execute(delete(User).where(User.id == registered.json()["id"]))
        await session.commit()

    response = await api_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
