from fastapi import APIRouter, Depends, Request, Security
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException

from src.database import get_async_session
from src.auth.schema import SignUp, Tokens, Login
from src.auth.service import get_auth_service, AuthService
from src.config import REFRESH_TTL
from src.auth.security import check_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup", response_model=Tokens)
async def signup(signup: SignUp,
                 request: Request,
                 response: Response, 
                 session: AsyncSession = Depends(get_async_session),
                 service: AuthService = Depends(get_auth_service)):
    
    user_agent = request.headers.get("user-agent")

    tokens = await service.signup(session, signup, user_agent)

    response.set_cookie(key="refresh_token", 
                        value=tokens.refresh_token, 
                        httponly=True, max_age=REFRESH_TTL, secure=True)

    return tokens

@router.post("/refresh", response_model=Tokens)
async def refresh(request: Request, response: Response,
                  session: AsyncSession = Depends(get_async_session),
                  service: AuthService = Depends(get_auth_service)):
    
    token = request.cookies.get("refresh_token")

    if token is None:
        raise HTTPException(status_code=401, detail="Refresh token not provided")
    
    tokens = await service.refresh(session, token)

    response.set_cookie(key="refresh_token", 
                        value=tokens.refresh_token, 
                        httponly=True, max_age=REFRESH_TTL, secure=True)
    return tokens

@router.post("/login", response_model=Tokens)
async def login(login: Login,
                request: Request,
                response: Response, 
                session: AsyncSession = Depends(get_async_session),
                service: AuthService = Depends(get_auth_service)):
    
    user_agent = request.headers.get("user-agent")

    tokens = await service.login(session, login, user_agent)

    response.set_cookie(key="refresh_token", 
                        value=tokens.refresh_token, 
                        httponly=True, max_age=REFRESH_TTL, secure=True)

    return tokens

@router.delete("/logout", dependencies=[Security(check_access_token)])
async def logout(request: Request,
                 response: Response, 
                 session: AsyncSession = Depends(get_async_session),
                 service: AuthService = Depends(get_auth_service)):

    user_agent = request.headers.get("user-agent")

    email = request.state.user.email

    await service.logout(session, email, user_agent)

    response.delete_cookie("refresh_token", httponly=True, secure=True)

    return {"message": "ok"}

