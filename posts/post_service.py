from operator import or_

import sqlalchemy.orm as _orm
from fastapi import UploadFile, HTTPException
from sqlalchemy import and_
import random
import models as _models
import schemas as post_schema
import datetime as _dt

from utils import storage_service

PAGE_SIZE = 9


def get_posts_with_filters(db: _orm.Session, category: str = None, date: _dt.datetime = None, page: int = 0):
    limit = PAGE_SIZE
    offset = page * PAGE_SIZE
    query = db.query(_models.Post)
    if category:
        query = query.filter(_models.Post.category == category)
    if date:
        date = date + _dt.timedelta(days=1)
        query = query.filter(_models.Post.date_created <= date)
    print("ok1")
    query = query.order_by(_models.Post.date_last_updated.desc())
    posts = query.offset(offset).limit(limit).all()

    for post in posts:
        post.image_url = storage_service.get_link_file(post.image_key)
        post.bookmarks = db.query(_models.Bookmark).filter(_models.Bookmark.post_id == post.id).all()
        post.owner_id = db.query(_models.User).filter(_models.User.id == post.owner_id).first()
        post.owner_id.password = None

    return posts


def get_posts(db: _orm.Session, page: int):
    limit = page + 1 * PAGE_SIZE
    posts = db.query(_models.Post).limit(limit).all()
    for post in posts:
        post.image_url = storage_service.get_link_file(post.image_key)
        post.bookmarks = db.query(_models.Bookmark).filter(_models.Bookmark.post_id == post.id).all()
        post.owner_id = db.query(_models.User).filter(_models.User.id == post.owner_id).first()
        post.owner_id.password = None
    return posts


def get_random_posts(db: _orm.Session, post_id: int, num_posts: int = 6):
    all_post_ids = [post.id for post in db.query(_models.Post).all()]
    # loại bài viết hiện tại
    all_post_ids.remove(post_id)

    random_post_ids = random.sample(all_post_ids, num_posts)
    random_posts = db.query(_models.Post).filter(_models.Post.id.in_(random_post_ids)).all()

    if len(random_posts) != num_posts:
        pass

    for post in random_posts:
        post.image_url = storage_service.get_link_file(post.image_key)
        post.bookmarks = db.query(_models.Bookmark).filter(_models.Bookmark.post_id == post.id).all()
        post.owner_id = db.query(_models.User).filter(_models.User.id == post.owner_id).first()
        post.owner_id.password = None

    return random_posts


def checkFileImage(file: UploadFile):
    if file.content_type.split('/')[1] not in ['jpeg', 'png', 'jpg', 'webp']:
        return False
    return True


def checkSizeImage(file: UploadFile):
    if file.size > 8 * 1024 * 1024:
        return False
    return True


def create_post(db: _orm.Session, post: post_schema.PostCreate, user_id: int):
    post = _models.Post(**post.dict(), owner_id=user_id,
                        date_created=_dt.datetime.now(),
                        date_last_updated=_dt.datetime.now())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: _orm.Session, post_id: int):
    post = db.query(_models.Post).filter(_models.Post.id == post_id).first()
    post.image_url = storage_service.get_link_file(post.image_key)
    post.bookmarks = db.query(_models.Bookmark).filter(_models.Bookmark.post_id == post.id).all()
    post.owner_id = db.query(_models.User).filter(_models.User.id == post.owner_id).first()
    post.owner_id.password = None
    return post


def get_post_by_id(db: _orm.Session, post_id: int):
    return db.query(_models.Post).filter(_models.Post.id == post_id).first()

def delete_post_no_user(db: _orm.Session, post_id: int):
    post = db.query(_models.Post).filter(_models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
def delete_post(db: _orm.Session, post_id: int, user_id: int):
    print(user_id)
    post = db.query(_models.Post).filter(_models.Post.id == post_id, _models.Post.owner_id == user_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found or user is not owner of post")
    storage_service.delete_file(post.image_key)
    db.delete(post)
    db.commit()


def update_post(db: _orm.Session, post_id: int, file: UploadFile, user_id: int, post: post_schema.PostCreate):
    findPost = db.query(_models.Post).filter(_models.Post.id == post_id, _models.Post.owner_id == user_id).first()
    if findPost is None:
        raise Exception(status_code=400, detail="Post not found")
    if not checkFileImage(file):
        raise Exception(status_code=400, detail="File is not image")
    if not checkSizeImage(file):
        raise Exception(status_code=400, detail="File is too large. Max size is 8MB")
    storage_service.delete_file(findPost.image_key)
    image_key = storage_service.upload_file(file)
    image_url = storage_service.get_link_file(image_key)
    findPost.image_key = image_key
    findPost.image_url = image_url
    findPost.title = post.title
    findPost.description = post.description
    findPost.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(findPost)
    return findPost


def get_post_by_user(db: _orm.Session, user_id: int):
    return db.query(_models.Post).filter(_models.Post.owner_id == user_id).all()
