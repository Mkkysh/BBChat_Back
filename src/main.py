from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.test.auth_test_router import router as test_auth_router
from src.test.test import router as test_router

app = FastAPI(root_path="/api")

app.include_router(auth_router)
app.include_router(test_auth_router)
app.include_router(test_router)
