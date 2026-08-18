"""
    modello Spot: 
        persistenza, round-trip delle coordinate e vincoli (nome, posizione, proprietario)
"""
import pytest
from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.models.spot import Spot
from app.models.user import User
from app.services.auth import hash_password

# WKT(Well-Known Text):  "POINT(lan lat)"
POINT = WKTElement("POINT(11.5, 44.5)", srid=4326)

async def _create_owner(db_session) -> User:
    """Crea e restituisce un utente proprietario per gli spot"""
    user = User(email="owner@example.com", hashed_password=hash_password("password"))

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

async def test_post_perists_and_reads_back(db_session):
    """Crea uno spot, lo rilegge e verifica tutti i campi"""
    owner = _create_owner(db_session)

    spot = Spot(
            name="Test Spot",
            location=POINT,
            user_id=owner.id
    )
    db_session.add(spot)
    await db_session.commit()
    await db_session.refresh(spot)

    # rilettura da db con query
    result = await db_session.execute(select(Spot).where(Spot.id == spot.id))
    saved = result.scalar_one()

    assert saved.name == "Test Spot"
    assert saved.location == POINT
    assert saved.user_id == owner.id

async def test_spot_location_roundtrip_coordinates(db_session): 
    """Le coordinate salvate tornano identiche"""
    owner = await _create_owner(db_session)

    spot = Spot(
        name="Bosco", 
        location=POINT,
        user_id=owner.id
    )
    db_session.add(spot)
    await db_session.commit()

    # ST_AsText(postGis) converte la geometria in WKT
    result = await db_session.execute(
        select(func.ST_AsText(Spot.location)).where(Spot.id == spot.id)
    )
    assert result.scalar_one() == "POINT(11.5 44.5)"

async def test_spot_requires_name(db_session):
    owner = await _create_owner(db_session)
    db_session.add(Spot(name=None, location=POINT, user_id = owner.id))
    with pytest.raises(IntegrityError):
        await db_session.commit()

async def test_spot_requires_location(db_session):
    owner = await _create_owner(db_session)
    db_session.add(Spot(name="Test Spot", location=None, user_id = owner.id))
    with pytest.raises(IntegrityError):
        await db_session.commit()

async def test_spot_requires_owner(db_session):
    db_session.add(Spot(name="Test Spot", location=POINT, user_id=None))
    with pytest.raises(IntegrityError):
        await db_session.commit()

async def test_spot_custom_radius_persists(db_session):
    """Un raggio personalizzato viene salvato e riletto correttamnte"""
    owner = await _create_owner(db_session)

    spot = Spot(
        name="Test Spot",
        location=POINT,
        radius=1000,
        user_id=owner.id
    )
    db_session.add(spot)
    await db_session.commit()

    result = await db_session.execute(select(Spot).where(Spot.id == spot.id))
    saved = result.scalar_one()

    assert saved.radius == 1000

    