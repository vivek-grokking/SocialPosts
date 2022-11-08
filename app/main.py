from .routers import post, user, auth
from . import models, schemas, utils
from .database import engine
from fastapi import FastAPI

# creates the tables from 'models' if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()    

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def hello_world():
    return {"message": "Welcome to best Social Media application in the world ! :)"}