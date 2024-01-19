from fastapi import Security, Request, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import time
import jwt
from datetime import timedelta
from typing import Any
import uuid
from enum import Enum, unique

from src.database import get_async_session
from src.config import JWT_SECRET, ALGORITHM
from src.user.model import User


@unique
class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'

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
    
    try:
        if payload['type'] != TokenType.ACCESS.value:
            raise HTTPException(status_code=401, detail="token is invalid")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token is invalid")

    
    user = await session.scalar(select(User)
                                .where(User.email == payload["email"]))

    if user is None:
        raise HTTPException(status_code=401, detail="token is invalid")
    
    print(user)

    request.state.user = user

    await session.commit()

    return authorization_header


def sign_token(
    type: str, subject: str,
    payload: dict[str, Any]={},
    ttl: timedelta=None
) -> str:
    """
    Keyword arguments:
    type -- тип токена(access/refresh);
    subject -- субъект, на которого выписывается токен;
    payload -- полезная нагрузка, которую хочется добавить в токен;
    ttl -- время жизни токена
    """
    current_timestamp = time.time()
        
    data = dict(
 
        iss='bb@authservice',
        sub=subject,
        type=type,
   
        jti=str(uuid.uuid4()),
  
        iat=current_timestamp, 

        nbf=payload['nbf'] if payload.get('nbf') else current_timestamp
    )

    data.update(dict(exp=data['nbf'] + int(ttl.total_seconds()))) if ttl else None

    payload.update(data)
    
    return jwt.encode(payload=payload, key=JWT_SECRET, algorithm=ALGORITHM)

