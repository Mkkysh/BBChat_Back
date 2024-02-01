from sqlalchemy import Table, Column, Integer, String, MetaData, BOOLEAN, ForeignKey, func

from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.user.model import User

from datetime import datetime

class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    private: Mapped[bool]

    users: Mapped[List["User"]] = relationship(
        back_populates="rooms",
        secondary="userRoom"
    )

    messages: Mapped[List["Message"]] = relationship(
        back_populates="room"
    )

class UserRoom(Base):
     __tablename__ = "userRoom"

     user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
     room_id: Mapped[int] = mapped_column(ForeignKey("room.id", ondelete="CASCADE"), primary_key=True)

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    isEdit: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    isRead: Mapped[bool] =  mapped_column(default=False)
    isAudio: Mapped[bool] = mapped_column(default=False)
    idUser: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    idRoom: Mapped[int] = mapped_column(ForeignKey("room.id", ondelete="CASCADE"))
    room: Mapped["Room"] = relationship(back_populates="messages")
    user: Mapped["User"] = relationship(back_populates="messages")

