from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str]
    name: str
    username: str
    email: str
    password: str
    super: bool
    active: bool