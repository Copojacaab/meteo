"""
    id: chiave unica
    email: identificativo di login, unico
    hashed_password: output di argon2
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base

class User(Base):
    __tablename__ = "users"

    #  Attr
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] =  mapped_column(String(255), nullable=False)
