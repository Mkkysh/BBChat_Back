from pydantic import BaseModel
from typing import Optional, List
from src.user.model import User

class CreateRoom(BaseModel):
    name: Optional[str] = None
    members: List[int]

class UserResponseRoom(BaseModel):
    id: int
    name: str
    email: str

class ResponseRoom(BaseModel):
    id: int
    name: str | None
    private: bool
    members: List[UserResponseRoom]