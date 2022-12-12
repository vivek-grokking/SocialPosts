from .routers import post, user, auth, vote
from . import models
from .database import engine
from fastapi import FastAPI
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# creates the tables from 'models' if not exists
# not needed as Almebic takes care of it
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()    

origins = ["*"]  # only for test and dev environments

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def hello_world():
    return {"message": "Hello there !)"}
