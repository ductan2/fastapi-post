from typing import Union

import sqlalchemy.orm as _orm
import uuid

import models as _models
import schemas as user_schema
from passlib.context import CryptContext
from sqlalchemy import or_

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def create_user_google(db: _orm.Session, user):
    unique_id = f'${uuid.uuid4()}'
    hash_password = pwd_context.hash(unique_id)
    db_user = _models.User(email=user['email'], username=user['name'], password=hash_password, google=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: _orm.Session, email: str) -> _models.User:
    return db.query(_models.User).filter(_models.User.email == email).first()


def get_user_by_username(db: _orm.Session, username: str) -> _models.User:
    return db.query(_models.User).filter(_models.User.username == username).first()


def get_user_by_username_and_email(db: _orm.Session, username: str, email: str) -> Union[_models.User, None]:
    return (db.query(_models.User).filter(_models.User.username == username, _models.User.email == email)
            .options(_orm.joinedload(_models.User.bookmarks)).first())


def get_user_by_email_or_username(db: _orm.Session, identifier: str) -> Union[_models.User, None]:
    return db.query(_models.User).filter(
        or_(_models.User.email == identifier, _models.User.username == identifier)).first()


def create_user(db: _orm.Session, user: user_schema.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = _models.User(email=user.email, username=user.username, password=hashed_password, google=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
