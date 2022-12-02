from .routers import post, user, auth
from . import models
from .database import engine
from fastapi import FastAPI
from .config import settings

# creates the tables from 'models' if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()    

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") 
def hello_world():
    return {"message": "Hello there !)"}