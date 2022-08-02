from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from ..config.db import conn
from bson.objectid import ObjectId
from .schemas import albumEntity


class Album(BaseModel):
    username: Optional[str]
    title: Optional[str] = 'Album'
    is_active: Optional[bool] = True
    created: Optional[datetime] = None
    cover: Optional[str] = None
    is_public: Optional[bool] = False
    shared_with: Optional[list[EmailStr]] = []
    photos: Optional[list[str]]= []
    
    def save(self):
        id = conn.local.albums.insert_one(dict(self)).inserted_id
        return id

    def get_one(id):
        album = albumEntity(conn.local.albums.find_one({'_id':ObjectId(id)}))
        return album

  