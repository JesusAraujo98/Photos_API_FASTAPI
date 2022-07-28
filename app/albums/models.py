from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime



class Album(BaseModel):
    username: Optional[str]
    title: Optional[str] = 'Album'
    is_active: Optional[bool] = True
    created: Optional[datetime] = None
    cover: Optional[str] = None
    is_public: Optional[bool] = False
    shared_with: Optional[list[EmailStr]] = []
    photos: Optional[list[str]]= []
    

    
