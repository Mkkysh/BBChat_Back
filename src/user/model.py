from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from typing import List
from src.auth.model import RefreshToken

metadata = MetaData()

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="users",
        secondary="refreshTokenUser"
    )