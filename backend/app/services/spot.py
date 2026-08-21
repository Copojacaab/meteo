"""
    Service Spot: business logic per gli spot con controllo di ownership. Permette di
        - creare uno spot
        - leggere un proprio spot
        - listare solo i propri spot
        - modificare un proprio spot
        - cancellare un proprio spot
        Un utente diverso non deve poter leggere, modificare o cancellare lo spot

        Il controllo deve essere applicato nel service tramite la coppia:
            - Spot.id == spot_id
            - Spot.user_id == user_id
"""
from geoalchemy2.elements import WKTElement
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.spot import Spot

def _to_wkt(longitude: float, latitude: float) -> WKTElement:
    # WKT: POINT(longitude latitude)
    return WKTElement(f"POINT({longitude} {latitude})", srid=4326)



async def get_spot_by_id(
        session: AsyncSession,
        user_id: int,
        spot_id: int,
) -> Spot | None:
    result = await session.execute(
        select(Spot).where(Spot.id == spot_id, Spot.user_id == user_id)
        )

    return result.scalar_one_or_none()

async def list_spot_by_owner(
        session: AsyncSession,
        user_id: int
) -> list[Spot]:
    result = await session.execute(
        select(Spot).where(Spot.user_id == user_id).order_by(Spot.id)
    )
    return list(result.scalars().all())

    
async def create_spot(
        session: AsyncSession,
        user_id: int,
        name: str,
        longitude: float,
        latitude: float,
        radius: int=500) -> Spot:
    
    spot = Spot(
        name=name,
        location=_to_wkt(longitude, latitude),
        radius=radius,
        user_id=user_id
    )

    session.add(spot)
    await session.commit()
    await session.refresh(spot)

    return spot




async def delete_spot(
        session: AsyncSession,
        user_id: int,
        spot_id: int) -> bool:

    spot = await get_spot_by_id(session, user_id, spot_id)

    if spot is None:
        return False

    await session.delete(spot)
    await session.commit()
    return True
