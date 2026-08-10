"""
    Dipendenze FastAPI per l'autenticazione.

    get_current_user decodifica il JWT bearer e carica l'utente:
    token assente, invalido o scaduto -> 401 con WWW-Authenticate: Bearer.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.services.auth import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    subject = payload.get("sub")
    if subject is None or not subject.isdigit():
        raise credentials_exception

    user = await db.get(User, int(subject))
    if user is None:
        raise credentials_exception

    return user
