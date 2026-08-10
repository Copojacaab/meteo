"""
    Step 2.2 — persistenza del modello User:
    CRUD base, vincolo di unicita' su email, timestamp popolati dal DB.
"""
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.services.auth import hash_password


async def test_user_persists_and_reads_back(db_session):
    user = User(email="user@example.com", hashed_password=hash_password("secret123"))
    db_session.add(user)
    await db_session.commit()

    result = await db_session.execute(select(User).where(User.email == "user@example.com"))
    saved = result.scalar_one()

    assert saved.id is not None
    assert saved.hashed_password == user.hashed_password
    assert saved.created_at is not None
    assert saved.updated_at is not None


async def test_email_unique_constraint_rejects_duplicate(db_session):
    db_session.add(User(email="dup@example.com", hashed_password=hash_password("secret123")))
    await db_session.commit()

    db_session.add(User(email="dup@example.com", hashed_password=hash_password("other456")))
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_required_fields_cannot_be_null(db_session):
    db_session.add(User(email="nohash@example.com", hashed_password=None))
    with pytest.raises(IntegrityError):
        await db_session.commit()
