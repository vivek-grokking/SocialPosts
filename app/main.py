from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # optional field
    rating: Optional[int] = None

HOST = 'localhost'
DATABASE = 'social-fastapi'
USER = 'postgres'
PASSWORD = ''

while True:
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, 
        password=PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection established !')
        break
    except Exception as error:
        print('Database connection failed. Error: ', error)   
        time.sleep(5)
        print('Retrying database connection...') 

@app.get("/")
def hello_world():
    return {"message": "Welcome to best Social Media application in the world ! :)"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts;  """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    # extract all variables from Body and store in variable called "payload"
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ; """, 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int): # adding "int" to input param provides type-validation
    cursor.execute(""" SELECT * FROM posts WHERE id = %s ;""", (str(id),)) # trailing comma after str(id) is important
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f"post with id {id} was not found")
    return {"data": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * ; """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit;
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ; """, 
    (post.title, post.content, post.published, str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail= f"post with id {id} does not exists")
    return {"data": updated_post}