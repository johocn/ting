from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    phone: str

class UserLogin(BaseModel):
    username: str
    password: str
