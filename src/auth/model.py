from sqlalchemy import Table, Column, Integer, String, MetaData, BOOLEAN, ForeignKey

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.user.model import User

metadata = MetaData()

class RefreshToken(Base):
    __tablename__ = "refreshToken"

    jti: Mapped[str] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(nullable=False)
    rewoked: Mapped[bool] = mapped_column(nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[List["User"]] = relationship(
        back_populates="tokens",
        secondary="refreshTokenUser"
    )

class RefreshTokenUser(Base):
    __tablename__ = "refreshTokenUser"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    refresh_token_jti: Mapped[str] = mapped_column(ForeignKey("refreshToken.jti", ondelete="CASCADE"), primary_key=True)
    
