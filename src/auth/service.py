from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from fastapi import HTTPException

from src.auth.schemas import SignUp
from src.auth.hasher import pwd_context
from src.user.model import User

class AuthService:
    async def signup(self, session: AsyncSession, signup: SignUp):
        userQuery = select(User).where(User.c.email == signup.email)
        user = await session.execute(userQuery)
        if user.first() is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        data = signup.model_dump().copy()
        data['password'] = pwd_context.hash(data['password'])

        stmt = insert(User).values(**data)

        await session.execute(stmt)
        await session.commit()

authService = AuthService()