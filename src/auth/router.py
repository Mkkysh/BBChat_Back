from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.auth.schemas import SignUp
from src.auth.service import authService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup")
async def signup(signup: SignUp, 
                 session: AsyncSession = Depends(get_async_session)):
    await authService.signup(session, signup)
    return JSONResponse(status_code=201,
                        content={"message": "ok"})