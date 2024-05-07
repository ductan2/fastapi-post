from fastapi import HTTPException, APIRouter
from sqlalchemy.orm import Session
import database as _database

from fastapi import APIRouter
import auth.jwt_handler as _jwt_handler
from http.client import HTTPException
import bookmarks.bookmark_service as _bookmark_service
from fastapi import Depends
import posts.post_service as _post_service

router = APIRouter();


@router.post("/create/{post_id}")
def add_bookmark(post_id: int,user=Depends(_jwt_handler.get_user_by_token), db: Session = Depends(_database.get_db)):

    if not _post_service.get_post_by_id(db, post_id):
        raise HTTPException(status_code=400, detail="Post not found")
    print(user)
    existing_bookmark = _bookmark_service.getBookmarkByUserAndPost(db, user_id=user.id, post_id=post_id)
    if existing_bookmark:
        _bookmark_service.deleteBookmark(db, existing_bookmark.id)
        return {"message": "Bookmark delete successfully"}
    else:
        _bookmark_service.createBookmark(db, user_id=int(user.id), post_id=int(post_id))
        return {"message": "Bookmark added successfully"}


@router.get("/user")
def get_bookmarks_by_user(user=Depends(_jwt_handler.get_user_by_token), db: Session = Depends(_database.get_db)):
    return _bookmark_service.getBookmarkByUser(db, user.id)

