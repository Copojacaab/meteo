"""
    Modello Spot: uno spot di raccolta con posizione GPS.

    Spot appartiene a un utente (user_id), ha un nome (name), e un punto geografico (location)
        (lat, lon in WGS84) e un raggio (radius) in metri attorno a quel punto.
"""
from datetime import datetime

from geoalchemy2 import WKBElement, Geography
from sqlalchemy import String, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base


class Spot(Base):
    __tablename__ = "spots"

    # Attr
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    #   Posizione: POINT in WGS84 (SRID 4326)
    #       geography: distanze in metri funzionano direttamente
    #       Mapped[WKBElement] = tipo che geoalchemy2 usa per r/w
    location: Mapped[WKBElement] = mapped_column(
            Geography(geometry_type="POINT", srid=4326), 
            nullable=False
        )
    radius: Mapped[int] = mapped_column(Integer, nullable=False, default=500)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
