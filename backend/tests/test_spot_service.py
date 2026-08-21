"""
    Service Spot: creazione, ownership e query spaziale
"""

import pytest
from sqlalchemy import func, select

from app.models.spot import Spot
from app.services.spot import create_spot, get_spot_by_id, list_spot_by_owner

async def test_create_spot_persists_with_default_radius(db_session, owner):
    spot = await create_spot(
            session=db_session,
            user_id=owner.id,
            name="Test Spot",
            longitude=11.5, latitude=44.5
            )

    assert spot.id is not None
    assert spot.name == "Test Spot"
    assert spot.radius == 500
    assert spot.user_id == owner.id


async def test_create_spot_custom_radius(db_session, owner):
    spot = await create_spot(
            session=db_session,
            user_id=owner.id,
            name="Test Spot",
            longitude=11.5, latitude=44.5,
            radius=1000
            )

    assert spot.radius == 1000

async def test_create_spot_roundtrip_coordinates(db_session, owner):
    """Le coordinate tornano identiche da PostGIS (ST_AsText)"""
    await create_spot(db_session, owner.id, "Test Spot", 11.5, 44.5)

    result = await db_session.execute(
        select(func.ST_AsText(Spot.location)).where(Spot.name == "Test Spot")
    )

    assert result.scalar_one() == "POINT(11.5 44.5)"



# --- Lettura con controllo ownership ---

async def test_get_spot_by_id_return_own_spot(db_session, owner):
    spot = await create_spot(db_session, owner.id, "Mio Spot", 11.5, 44.5)

    found = await get_spot_by_id(db_session, owner.id, spot.id)

    assert found is not None
    assert found.name == "Mio Spot"
    assert found.id == spot.id

async def test_get_spot_by_id_denies_other_user(db_session, owner, other_owner):
    spot = await create_spot(db_session, owner.id, "Mio Spot", 11.5, 44.5)

    found = await get_spot_by_id(db_session, other_owner.id, spot.id)

    assert found is None

async def test_get_spot_by_id_return_none_for_missing(db_session, other_owner):
    found = await get_spot_by_id(db_session, other_owner.id, spot_id=1)

    assert found is None

async def test_list_spot_by_owner_returns_only_own(db_session, owner, other_owner):
    await create_spot(db_session, owner.id, "Spot A", 11.5, 44.5)
    await create_spot(db_session, owner.id, "Spot B", 11.6, 44.6)

    await create_spot(db_session, other_owner.id, "Spot 1", 12.0, 45.0)

    spots = await list_spot_by_owner(db_session, owner.id)

    assert len(spots) == 2
    assert all(s.user_id == owner.id for s in spots)

# --- Aggiornamento (crUd) Spot ---

async def test_update_spot_changes_owner_spot(db_session, owner):
    spot = await create_spot(db_session, owner.id, "Vecchio Nome", 11.5, 44.5,)

    updated = await update_spot(
        session=db_session,
        user_id=owner.id,
        spot_id=spot.id,
        new_name="Nuovo Nome",
        new_lon=11.6, 
        new_lat=44.6,
        new_radius=1000
    )

    assert updated is not None
    assert updated.name == "Nuovo Nome" 
    assert updated.radius == 1000

    result = await db_session.execute(
        select(
            func.As_Text(Spot.location).where(Spot.id==spot.id,Spot.user_id==owner.id)
            ))

    assert result.scalar_one() == "POINT(11.6 44.6)"

# --- Aggiornamento con controllo ownership ---

async def test_update_spot_denies_other_user(db_session, owner, other_owner):
    spot = await create_spot(
        db_session, 
        owner.id,
        "Mio Spot",
        11.5, 
        44.5,
    )

    updated = await update_spot(
        db_session,
        other_owner.id,
        spot.id,
        "Spot Modificato",
        12.0,
        45.0,
        2000,
    )

    assert updated is None

    found = await get_spot_by_id(
        db_session,
        owner.id,
        spot.id
    )

    assert found is not None
    assert found.name == "Mio Spot"
    
    result = await db_session.execute(
        select(func.AsText(Spot.location).where(Spot.id==spot.id, Spot.user_id==owner.id))
    )

    assert result.scalar_one() == "POINT(11.5 44.5)"

    assert found.radius == 500

# --- Cancellazione (cruD) Spot ---

from app.services.spot import delete_spot

async def test_delete_spot_removes_owner_spot(db_session, owner):
    spot = await create_spot(
        db_session,
        owner.id,
        "Da Eliminare",
        11.5,
        44.5,
    )

    deleted = await delete_spot(
        session=db_session,
        user_id=owner.id,
        spot_id=spot.id,
    )

    assert deleted is True
    assert await get_spot_by_id(db_session, owner.id, spot.id) is None

# --- Cancellazione con controllo ownership ---

async def test_delete_spot_denies_other_user(db_session, owner, other_owner):
    spot = await create_spot(
        db_session, 
        owner.id,
        "Mio Spot",
        11.5, 
        44.5,
    )

    deleted = await delete_spot(
        db_session,
        other_owner.id,
        spot.id,
    )

    assert deleted is False
    assert await get_spot_by_id(db_session, owner.id, spot.id) is not None
    