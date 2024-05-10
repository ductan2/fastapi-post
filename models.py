import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String(255), unique=True, index=True)
    username = _sql.Column(_sql.String(255), unique=True, index=True)
    password = _sql.Column(_sql.String(255))
    google = _sql.Column(_sql.Boolean, default=False)
    posts = _orm.relationship("Post", back_populates="owner")
    bookmarks = _orm.relationship("Bookmark", back_populates="user")


class Post(_database.Base):
    __tablename__ = "posts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String(100), index=True)
    image_key = _sql.Column(_sql.String(1000))
    image_url = _sql.Column(_sql.String(1000))
    description = _sql.Column(_sql.String(1000), index=True)
    category = _sql.Column(_sql.String(100), index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    bookmarks = _orm.relationship("Bookmark", back_populates="post")
    owner = _orm.relationship("User", back_populates="posts")


class Bookmark(_database.Base):
    __tablename__ = 'bookmarks'
    id = _sql.Column(_sql.Integer, primary_key=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'), nullable=False)
    post_id = _sql.Column(_sql.Integer, _sql.ForeignKey('posts.id'), nullable=False)

    user = _orm.relationship("User", back_populates="bookmarks")
    post = _orm.relationship("Post", back_populates="bookmarks")
