from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from typing import List

from typing import TYPE_CHECKING


from src.auth.model import RefreshToken
from src.chat.model import Room, Message

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

    rooms: Mapped[List["Room"]] = relationship(
        back_populates="users",
        secondary="userRoom"
    )

    messages: Mapped[List["Message"]] = relationship(
        back_populates="user"
    )