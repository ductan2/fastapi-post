
import fastapi as _fastapi
import database
from bookmarks import bookmark_router
from users import user_router
import utils.file_s3 as file_s3
from fastapi.middleware.cors import CORSMiddleware
import posts.post_router as post_router
app = _fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database.create_database()
app.include_router(file_s3.router, prefix="/file", tags=["files"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(post_router.router, prefix="/posts", tags=["posts"])
app.include_router(bookmark_router.router, prefix="/bookmarks", tags=["bookmarks"])
