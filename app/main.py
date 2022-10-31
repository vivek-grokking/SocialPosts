from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # optional field
    rating: Optional[int] = None

my_posts = [{'title':'title of post 1', 'content':'content of post 1', 'id':1},
            {'title':'favorite foods', 'content':'I like pizza', 'id':2},]

@app.get("/")
def hello_world():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    # extract all variables from Body and store in variable called "payload"
    post_dict = post.dict()
    post_dict['id'] = randint(0, 10000)
    my_posts.append(post_dict)
    return {"data":post_dict}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i    

@app.get("/posts/{id}")
def get_post(id: int): # adding "int" to input param provides type-validation
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f"post with id {id} was not found")
    return {"data": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    print(f'deleting id {id}')
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)     
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail= "post with id {id} does not exists")
    post_dict = post.dict()    
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}