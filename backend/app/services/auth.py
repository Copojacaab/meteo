"""
    Service auth: business logic di registrazione e autenticazione.

    Unico punto che conosce pwdlib (hash Argon2) e python-jose (JWT):
    i router chiamano queste funzioni senza sapere come funzionano.
"""
from datetime import UTC, datetime, timedelta

from jose import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User

ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def register_user(session: AsyncSession, email: str, password: str) -> User:
    user = User(email=email, hashed_password=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + expires_delta,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
