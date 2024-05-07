import sqlalchemy.orm as _orm

import models as _models
from utils import storage_service


def get_post_by_id(post_id: int):
    return _models.Post.query.filter_by(id=post_id).first()


def getBookmarkByUserAndPost(db: _orm.Session, user_id: int, post_id: int):
    return db.query(_models.Bookmark).filter(_models.Bookmark.user_id == user_id,
                                             _models.Bookmark.post_id == post_id).first()


def deleteBookmark(db: _orm.Session, bookmark: int):
    db.query(_models.Bookmark).filter(_models.Bookmark.id == bookmark).delete()
    db.commit()


def createBookmark(db: _orm.Session, user_id: int, post_id: int):
    bookmark = _models.Bookmark(user_id=user_id, post_id=post_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def getBookmarkByUser(db: _orm.Session, user_id: int):
    bookmarks = db.query(_models.Bookmark).filter(_models.Bookmark.user_id == user_id).all()
    return bookmarks


def getBookmarkByPost(db: _orm.Session, post_id: int):
    return db.query(_models.Bookmark).filter(_models.Bookmark.post_id == post_id).all()
