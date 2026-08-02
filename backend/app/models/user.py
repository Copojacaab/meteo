"""
    id: chiave unica
    email: identificativo di login, unico
    hashed_password: output di argon2
"""
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, func


from app.database import Base

class User(Base):
    __tablename__ = "users"

    #  Attr
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Meta
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

# Mapped[str] → colonna NOT NULL implicita.
# Mapped[str | None] (o Optional[str]) → colonna nullable.

