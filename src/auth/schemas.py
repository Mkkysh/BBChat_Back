from pydantic import BaseModel

class SignUp(BaseModel):
    name: str
    email: str
    password: str