from geoalchemy2 import WKTElement
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.spot import Spot

def _to_wkt(longitude: float, latidude: float) -> WKTElement:
    # WKT: POINT(lon lat)
    return WKTElement(f"POINT({longitude} {latidude})", srid=4326)

async def create_spot(
        session: AsyncSession,
        user_id: int,
        name: str,
        longitude: float,
        latitude: float,
        radius: int = 500
) -> Spot:
    spot = Spot(
        name=name,
        location=_to_wkt(longitude=longitude, latidude=latitude),
        radius=radius,
        user_id=user_id
    )

    session.add(spot)
    await session.commit()
    await session.refresh(spot)
    return spot