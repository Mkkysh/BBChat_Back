from fastapi import Security, Request, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt

from src.database import get_async_session
from src.config import JWT_SECRET, ALGORITHM
from src.user.model import User

async def check_access_token(
    request: Request,
    authorization_header: str = Security(APIKeyHeader(name='Authorization', auto_error=False)),
    session: AsyncSession = Depends(get_async_session)
) -> str:
    if authorization_header is None:
        raise HTTPException(status_code=401, detail="Authorization header not provided")
    
    if 'Bearer ' not in authorization_header:
        raise HTTPException(status_code=401, detail="Authorization header not provided")

    clear_token = authorization_header.replace('Bearer ', '')

    try:
        payload = jwt.decode(jwt=clear_token, key=JWT_SECRET, algorithms=ALGORITHM)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token is invalid")

    
    userQuery = select(User).where(User.c.email == payload['sub'])
    userAns = await session.execute(userQuery)
    user = userAns.first()

    if user is None:
        raise HTTPException(status_code=401, detail="token is invalid")

    request.state.user = user

    await session.commit()

    return authorization_header