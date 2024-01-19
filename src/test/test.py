from fastapi import APIRouter, Depends, Security, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.auth.security import check_access_token

router = APIRouter(
    prefix="/test",
    tags=["Test"]
    )

@router.get("/test")
async def signup(request: Request):
    user_agent = request.headers.get("user-agent")
    # Здесь вы можете обработать user-agent, чтобы определить устройство пользователя и приписать его к refresh токену
    return {"user_agent": user_agent}
