from pydantic import BaseModel

# pydantic model for schema
# they define the shape of the request / response objects

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # optional field

class PostCreate(PostBase):
    pass
