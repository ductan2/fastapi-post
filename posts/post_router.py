from datetime import datetime

import database
from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from fastapi import APIRouter, UploadFile, File, Form
import schemas as post_schema
from posts import post_service
import auth.jwt_handler as _jwt_handler
import utils.storage_service as _storage_service

router = APIRouter()


@router.post("/create")
def create_post(
        post: post_schema.PostCreate,
        db: _orm.Session = _fastapi.Depends(database.get_db),
        user=_fastapi.Depends(_jwt_handler.get_user_by_token)
):
    return post_service.create_post(db=db, post=post, user_id=user.id, )

@router.get('/random/{post_id}')
def get_random_posts(post_id: int, db: _orm.Session = _fastapi.Depends(database.get_db)):
    return post_service.get_random_posts(db=db, post_id=post_id)

@router.get('/user', response_model=List[post_schema.Post])
def get_post_by_user(user=_fastapi.Depends(_jwt_handler.get_user_by_token),
                     db: _orm.Session = _fastapi.Depends(database.get_db)):
    return post_service.get_post_by_user(db=db, user_id=user.id)


@router.get("/page/{page}")
def read_posts(
        page: int = 0,
        category: str = None,
        date: datetime = None,
        db: _orm.Session = _fastapi.Depends(database.get_db),
):
    print(date)
    posts = post_service.get_posts_with_filters(db=db, page=page, category=category,date=date)
    return posts


@router.get("/{post_id}")
def read_post(post_id: int, db: _orm.Session = _fastapi.Depends(database.get_db)):
    post = post_service.get_post(db=db, post_id=post_id)
    print(post)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this post does not exist"
        )
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(database.get_db),
                user=_fastapi.Depends(_jwt_handler.get_user_by_token)):
    post_service.delete_post(db=db, post_id=post_id, user_id=user.id)
    return {"message": f"successfully deleted post with id: {post_id}"}


@router.put("/{post_id}")
def update_post(
        post_id: int,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        user=_fastapi.Depends(_jwt_handler.get_user_by_token),
        db: _orm.Session = _fastapi.Depends(database.get_db),
):
    post = post_schema.PostCreate(title=title, description=description)
    return post_service.update_post(db=db, post=post, post_id=post_id, file=file, user_id=user.id)


@router.post('/upload')
async def uploadImage(file: UploadFile = File(...)):
    return await _storage_service.upload_file(file=file)


@router.get('/files/all')
async def getAllFile():
    return await _storage_service.getAllFile()


@router.get('/files/link')
async def getLinkAllFile():
    return await _storage_service.get_link_all_file()


@router.post('/files/upload')
async def uploadFile(file: UploadFile = File(...)):
    print(file)
    # if not post_service.checkFileImage(file):
    #     raise _fastapi.HTTPException(status_code=400, detail="File is not image")
    # if not post_service.checkSizeImage(file):
    #     raise _fastapi.HTTPException(status_code=400, detail="File is too large. Max size is 8MB")
    image_key = _storage_service.upload_file(file)
    image_url = _storage_service.get_link_file(image_key)
    return {
        "image_key": image_key,
        "image_url": image_url
    }
@router.delete('/delete/post/{post_id}')
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(database.get_db)):
    return post_service.delete_post_no_user(db=db, post_id=post_id)