from tokenize import group
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: Optional[str]
    last_name: Optional[str]
    is_staff: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True
    




