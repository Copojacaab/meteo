"""
    Service Spot: creazione, ownership e query spaziale
"""

import pytest
from sqlalchemy import func, select

from app.models.spot import Spot
from app.services.spots import create_spot

async def test_create_spot_persists_with_default_radius(db_session, owner):
    spot = await create_spot(
            db_session=db_session,
            name="Test Spot",
            user_id=owner.id,
            longitude=11.5, latitude=44.5
            )

    assert spot.id is not None
    assert spot.name == "Test Spot"
    assert spot.radius == 500
    assert spot.user_id == owner.id


async def test_create_spot_custom_radius(db_session, owner):
    spot = await create_spot(
            db_session=db_session,
            name="Test Spot",
            user_id=owner.id,
            longitude=11.5, latitude=44.5,
            radius=1000
            )

    assert spot.radius == 1000

async def test_create_spot_roundtrip_coordinates(db_session, owner):
    """Le coordinate tornano identiche da PostGIS (ST_AsText)"""
    await create_spot(db_session, "Test Spot", owner.id, 11.5, 44.5)

    result = await db_session.execute(
        func.ST_AsText(select(Spot.location).where(Spot.name == "Test Spot"))
        )

    assert result.scalar_one() == "POINT(11.5 44.5)"