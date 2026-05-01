from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    fname: str
    email: str
    password: str
    phone: str

class Login(BaseModel):
    email: str
    password: str