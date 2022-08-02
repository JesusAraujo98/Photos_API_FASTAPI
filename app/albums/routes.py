import os
import shutil
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from bson.objectid import ObjectId
from .models import Album
from .schemas import albumEntity,albumsEntity
from ..config.auth import AuthHandler
from ..config.db import conn
from ..config.s3uploader import s3_handler
from ..config.secrets import BUCKET_NAME


albums = APIRouter()
auth_handler = AuthHandler()



# @albums.put('/api/albums/share_options/{id}', tags = ['albums'], status_code = 200)
# async def share_options_album(id:str, public_option:bool=False, emails_list:list=[] ,username = Depends(auth_handler.auth_wrapper)):
#     album = conn.local.albums.find_one({'_id':ObjectId(id)})
#     album['is_public']= public_option
#     album['shared_with'].append(emails_list)
#     new_list = [str(email) for email in album['shared_with']] 
#     new_list = list(dict.fromkeys(new_list))

#     album['shared_with'] = new_list

#     return album


@albums.put('/api/albums/album_detail/{id}', tags = ['albums'], status_code=200)
async def update_single_album(id:str, updated_album:Album, username = Depends(auth_handler.auth_wrapper)):
    album = conn.local.albums.find_one({'_id':ObjectId(id)})
    if not album:
        status.status_code = status.HTTP_404_NOT_FOUND
        return {'message':'albums does not exists'}
    if username != album['username']:
        status.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': "invalid credentials"}
    
    if updated_album.title == '':
        updated_album.title == "album"

    album['title']= updated_album.title
    album['is_public'] = updated_album.is_public

    emails_list = [email for email in updated_album.shared_with]
    
    album['shared_with'] = emails_list
    
    conn.local.albums.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(album)})
    return id


    
@albums.get('/api/albums/album_detail/{id}', tags = ['albums'], status_code=200)
async def get_single_album(id:str, username = Depends(auth_handler.auth_wrapper)):
    # album = albumEntity(conn.local.albums.find_one({'_id':ObjectId(id)}))
    album = Album.get_one(id)

    if not album:
        status.status_code = status.HTTP_404_NOT_FOUND
        return {'message':'albums does not exists'}

    if username != album['username']:
        status.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': "invalid credentials"}
    
    return album


@albums.get('/api/albums/albums_details', tags = ['albums'], status_code=200)
async def get_all_user_albums(username = Depends(auth_handler.auth_wrapper)):
    return albumsEntity(conn.local.albums.find({'username':username}))


@albums.put('/api/albums/update_cover/{album_id}', status_code=200, tags=['albums'])
async def update_album_cover(album_id:str, file: UploadFile = File(...), username=Depends(auth_handler.auth_wrapper)):

    album = albumEntity(conn.local.albums.find_one({'_id':ObjectId(album_id)}))

    if not album:
        status.status_code = status.HTTP_404_NOT_FOUND
        return {'message':'albums does not exists'}

    if username != album['username']:
        status.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': "invalid credentials"}
    

    image_name = str(uuid.uuid4())+'.jpg'
    local_media_url = 'app/albums/media/'+image_name

    with open(local_media_url,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    s3_handler.upload_file(local_media_url, BUCKET_NAME ,image_name, ExtraArgs= {"ACL":"public-read"} )
    
    bucket_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/"+image_name
    album['cover'] = bucket_url
    album =conn.local.albums.find_one_and_update(
         {"_id": ObjectId(album_id)}, {"$set": dict(album)}
    )

    os.remove(local_media_url)
    return albumEntity(conn.local.albums.find_one({'_id':ObjectId(album_id)}))
    

@albums.post('/api/albums/create_album/', tags= ['albums'], status_code=200)
async def create_album(album:Album, username = Depends(auth_handler.auth_wrapper)):
    album.username = username
    album.created = str(datetime.now())
    id = album.save()
    
    return albumEntity(conn.local.albums.find_one({'_id':id}))


@albums.delete('/api/albums/delete/{id}', tags=['albums'], status_code=200)
async def delete_album(id:str):
    try:
        conn.local.albums.delete_one({'_id':ObjectId(id)})
        return {'message':'ok'}
    except:
        status.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Album does not exists'}
