from pydantic import BaseModel

class SignUp(BaseModel):
    name: str
    email: str
    password: str

class Tokens(BaseModel):
    access_token: str
    refresh_token: str