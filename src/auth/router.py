from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException

from src.database import get_async_session
from src.auth.schemas import SignUp, Tokens
from src.auth.service import get_auth_service, AuthService
from src.config import REFRESH_TTL


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup", response_model=Tokens)
async def signup(signup: SignUp,
                 response: Response, 
                 session: AsyncSession = Depends(get_async_session),
                 service: AuthService = Depends(get_auth_service)):
    tokens = await service.signup(session, signup)

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
