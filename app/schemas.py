from pydantic import BaseModel, EmailStr
from datetime import datetime

# pydantic model for schema
# they define the shape of the request / response objects
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # optional field

class PostCreate(PostBase):
    pass

# for response
class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str   

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True