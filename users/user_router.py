from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database as _database
import schemas as user_schema
from fastapi import APIRouter
import auth.jwt_handler as _jwt_handler
import users.user_service as user_service
from fastapi import Depends, Response
from decouple import config
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from utils.auth_google import get_user_info_from_google

oauth = OAuth2PasswordBearer(tokenUrl="token")
CLIENT_ID = config("GOOGLE_CLIENT_ID")
CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = config("GOOGLE_REDIRECT_URI")

router = APIRouter()


@router.post("/register", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(_database.get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Password does not match")
    print("user", user)
    if user_service.get_user_by_email(db=db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_service.get_user_by_username(db=db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user=user)


@router.post("/login", response_model=user_schema.UserResponse)
def login_user(user: user_schema.UserLogin, db: Session = Depends(_database.get_db), response: Response = Response()):
    print(user)
    db_user = user_service.get_user_by_email_or_username(db=db, identifier=user.emailOrUsername)
    print(db_user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid email or username")
    if not user_service.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    user_token = _jwt_handler.create_access_token(data={"sub": db_user.username})
    response.set_cookie(key="access_token", value=user_token, httponly=True)

    return {
        "user": db_user,
        "token": user_token
    }


@router.get("/current-user", response_model=user_schema.User)
def read_users_me(user=Depends(_jwt_handler.get_user_by_token)):
    return user


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/login/google")
async def login_google_redirect():
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20email%20profile&state=SOME_STATE"
    print(google_auth_url)
    return {"redirect_url": google_auth_url}


@router.get("/google-auth-callback")
async def google_auth_callback(code: str, db: Session = Depends(_database.get_db), response: Response = Response()):
    user_info = get_user_info_from_google(code)
    user_found = user_service.get_user_by_email(db=db, email=user_info['email'])
    user_token = _jwt_handler.create_access_token(data={"sub": user_info['name']})
    response.set_cookie(key="access_token", value=user_token, httponly=True)
    if user_found:
        return RedirectResponse(url=f"http://localhost:5173/login?token={user_token}&user={user_found}")
    new_user = user_service.create_user_google(db=db, user=user_info)
    return RedirectResponse(url=f"http://localhost:5173/login?token={user_token}&user={new_user}")
