from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from datetime import timedelta
import jwt

from src.config import JWT_SECRET, ALGORITHM, ACCESS_TTL, REFRESH_TTL
from src.auth.schemas import SignUp, Tokens, Login
from src.auth.hasher import pwd_context
from src.user.model import User
from src.auth.security import sign_token, TokenType
from src.auth.model import RefreshToken


class AuthService:
    async def signup(self, session: AsyncSession, signup: SignUp, user_agent: str):
        userQuery = select(User).where(User.email == signup.email)
        user = await session.execute(userQuery)
        if user.first() is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        data = signup.model_dump().copy()
        data['password'] = pwd_context.hash(data['password'])

        tokens = Tokens(
            access_token=sign_token(subject=signup.email, 
                                    type=TokenType.ACCESS.value, 
                                    ttl=timedelta(ACCESS_TTL), 
                                    payload={'email': signup.email,
                                             'user_agent': user_agent}),
            refresh_token=sign_token(subject=signup.email,
                                     type=TokenType.REFRESH.value,
                                     ttl=timedelta(REFRESH_TTL),
                                     payload={'email': signup.email,
                                              'user_agent': user_agent})
        )

        try:
            payload = jwt.decode(jwt=tokens.refresh_token, key=JWT_SECRET, algorithms=ALGORITHM)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="token is invalid")

        # stmtUser = insert(User).values(**data)

        user = User(**data)
        refreshToken = RefreshToken(jti=payload['jti'],token=tokens.refresh_token, rewoked=False,
                                    user_agent=user_agent)
        user.tokens.append(refreshToken)
        # stmtToken = insert(RefreshToken).values(token=tokens.refresh_token, 
        #                                         jti=payload['jti'],
        #                                         rewoked=True)
        

        # await session.execute(stmtUser)
        # await session.execute(stmtToken)

        session.add(user)
        await session.commit()

        return tokens
    
    async def refresh(self, session: AsyncSession, token: str):
        try:
            payload = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=ALGORITHM)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="token is invalid")
        
        if payload['type'] != TokenType.REFRESH.value:
            raise HTTPException(status_code=401, detail="token is invalid")
        
        token = await session.scalar(select(RefreshToken).
                                    where(RefreshToken.jti == payload['jti']).
                                    where(RefreshToken.user_agent == payload['user_agent']))
        token.rewoked = True

        users = await session.scalars(select(User)
                                    .where(User.email == payload['sub'])
                                    .options(selectinload(User.tokens)))
        user = users.first()

        tokens = Tokens(
            access_token=sign_token(subject=payload['email'], 
                                    type=TokenType.ACCESS.value, 
                                    ttl=timedelta(ACCESS_TTL), 
                                    payload={'email': payload['email'],
                                             'user_agent': payload['user_agent']}),
            refresh_token=sign_token(subject=payload['email'],
                                     type=TokenType.REFRESH.value,
                                     ttl=timedelta(REFRESH_TTL),
                                     payload={'email': payload['email'],
                                              'user_agent': payload['user_agent']})
        )

        try:
            payload = jwt.decode(jwt=tokens.refresh_token, key=JWT_SECRET, algorithms=ALGORITHM)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="token is invalid")

        refreshToken = RefreshToken(jti=payload['jti'],token=tokens.refresh_token, rewoked=False,
                                    user_agent=payload['user_agent'])
        user.tokens.append(refreshToken)

        await session.commit()

        return tokens
    
    async def login(self, session: AsyncSession, login: Login, user_agent: str):
        user = await session.scalar(select(User).where(User.email == login.email)
                                    .options(selectinload(User.tokens)))
        if user is None:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        if not pwd_context.verify(login.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        tokens = Tokens(
            access_token=sign_token(subject=login.email, 
                                    type=TokenType.ACCESS.value, 
                                    ttl=timedelta(ACCESS_TTL), 
                                    payload={'email': login.email,
                                             'user_agent': user_agent}),
            refresh_token=sign_token(subject=login.email,
                                     type=TokenType.REFRESH.value,
                                     ttl=timedelta(REFRESH_TTL),
                                     payload={'email': login.email,
                                              'user_agent': user_agent})
        )

        try:
            payload = jwt.decode(jwt=tokens.refresh_token, key=JWT_SECRET, algorithms=ALGORITHM)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="token is invalid")
        
        refreshToken = RefreshToken(jti=payload['jti'],token=tokens.refresh_token, rewoked=False,
                                    user_agent=user_agent)
        
        user.tokens.append(refreshToken)

        await session.commit()

        return tokens
    
    async def logout(self, session: AsyncSession, emall: str, user_agent: str):
        user = await session.scalar(select(User).where(User.email == emall)
                                    .options(selectinload(User.tokens)))
        
        tokens = await session.scalars(select(RefreshToken).where(RefreshToken.users.contains(user))
                                       .where(RefreshToken.user_agent == user_agent))
        
        user.tokens = [x for x in user.tokens if x not in tokens]

        await session.commit()

        return tokens




def get_auth_service() -> AuthService:
    return AuthService()