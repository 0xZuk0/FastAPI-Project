from fastapi import FastAPI
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .routers import post, users, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router
)
@app.get("/")
def home_page() :
    return {"status": "Hello World!"}



# @app.get("/test")
# def test_post(db: Session = Depends(get_db)) :
#     posts = db.query(models.Post).all()
#     return {"message": "Success!", "data": posts}
