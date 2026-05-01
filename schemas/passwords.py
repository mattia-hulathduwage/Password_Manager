from pydantic import BaseModel
from typing import Optional
from datetime import date

class Passwords(BaseModel):
    id: Optional[int] = None
    title: str
    user: str
    password: str
    last_updated: date