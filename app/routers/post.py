from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import models, schemas

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/",
        response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts;  """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, 
                    response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db)):
    # extract all variables from Body and store in variable called "payload"
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ; """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # this is sqlalchemy equivalent for " RETURNING *"

    return new_post

@router.get("/{id}")
def get_post(id: int, 
             db: Session = Depends(get_db)): # adding "int" to input param provides type-validation
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s ;""", (str(id),)) # trailing comma after str(id) is important
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f"post with id {id} was not found")
    return post

@router.delete("/{id}")
def delete_post(id: int, 
                db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * ; """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit;
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",
        response_model = schemas.Post)
def update_post(id: int, 
                post: schemas.PostCreate, 
                db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ; """, 
    # (post.title, post.content, post.published, str(id)),)
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail= f"post with id {id} does not exists")
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()            

    return post_query.first()