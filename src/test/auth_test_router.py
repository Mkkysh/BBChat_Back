from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.auth.security import check_access_token
from src.auth.schemas import SignUp
from src.auth.service import authService

router = APIRouter(
    prefix="/test/auth",
    tags=["Test.Auth"],
    dependencies=[Security(check_access_token)]
    )

@router.post("/token")
async def signup(session: AsyncSession = Depends(get_async_session)):
    return JSONResponse(status_code=200,
                        content={"message": "ok"})
