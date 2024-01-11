from fastapi import FastAPI

from src.auth.router import router as auth_router

app = FastAPI(root_path="/api")

app.include_router(auth_router)
