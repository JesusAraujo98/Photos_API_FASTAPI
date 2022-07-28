from fastapi import APIRouter, Depends, Response, status, Form, File, UploadFile
from .models import User
from ..config.db import conn
from passlib.hash import sha256_crypt
from ..config.auth import AuthHandler
from .schemas import userEntity
from pydantic import EmailStr

auth_handler = AuthHandler()


users = APIRouter()



@users.get('/api/users/', tags=['users'])
async def user_details(username=Depends(auth_handler.auth_wrapper)):
    return userEntity(conn.local.users.find_one({"username": username}))


@users.post('/api/users/login/', tags=['users', 'login'], status_code=200)
async def login(response: Response, email: EmailStr = Form(), password: str = Form()):

    registered_user = conn.local.users.find_one({'email': email})

    if not registered_user or (not auth_handler.verify_password(password, registered_user['password'])):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'invalid email or password'}

    token = auth_handler.encode_token(registered_user['username'])
    return {'token': token}


@users.post('/api/users/signup/', tags=['users'], status_code=201)
async def create_user(response: Response, email: EmailStr = Form(), username: str = Form(), password: str = Form()):
    registered_user = conn.local.users.find_one({"username": username})
    registered_email = conn.local.users.find_one({"email": email})

    if registered_user or registered_email:
        response.status_code = status.HTTP_409_CONFLICT
        return {'message': 'email and/or username already exists'}

    user = User(username=username, email=email, password=password)
    user.password = auth_handler.get_password_hash(user.password)

    id = conn.local.users.insert_one(dict(user)).inserted_id
    return {'message': 'message'}
