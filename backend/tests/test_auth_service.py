"""
    Step 2.3 — service auth:
    registrazione con hash Argon2, verifica password, credenziali valide/errate,
    contenuto del JWT.
"""
from datetime import UTC, datetime, timedelta

from jose import jwt

from app.config import settings
from app.services.auth import (
    ALGORITHM,
    authenticate_user,
    create_access_token,
    hash_password,
    register_user,
    verify_password,
)


async def test_register_user_stores_argon2_hash(db_session):
    user = await register_user(db_session, "new@example.com", "secret123")

    assert user.id is not None
    assert user.hashed_password != "secret123"
    assert user.hashed_password.startswith("$argon2")


def test_verify_password_accepts_correct_and_rejects_wrong():
    hashed = hash_password("secret123")

    assert verify_password("secret123", hashed)
    assert not verify_password("wrong-password", hashed)


async def test_authenticate_user_with_valid_credentials(db_session):
    await register_user(db_session, "user@example.com", "secret123")

    user = await authenticate_user(db_session, "user@example.com", "secret123")

    assert user is not None
    assert user.email == "user@example.com"


async def test_authenticate_user_with_wrong_password(db_session):
    await register_user(db_session, "user@example.com", "secret123")

    assert await authenticate_user(db_session, "user@example.com", "nope") is None


async def test_authenticate_user_with_unknown_email(db_session):
    assert await authenticate_user(db_session, "ghost@example.com", "secret123") is None


def test_access_token_contains_subject_and_default_expiry():
    token = create_access_token(42)

    payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    expires_at = datetime.fromtimestamp(payload["exp"], tz=UTC)

    assert payload["sub"] == "42"
    assert timedelta(minutes=29) < expires_at - datetime.now(UTC) <= timedelta(minutes=30)


def test_access_token_supports_custom_expiry():
    token = create_access_token(42, expires_delta=timedelta(minutes=-5))

    # exp nel passato: la verifica va disattivata per leggere il payload
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM],
        options={"verify_exp": False},
    )

    assert payload["sub"] == "42"
