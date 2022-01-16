from pyexpat import model
from statistics import mode
from typing import List
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search : Optional[str] = "") :
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)) :
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *; """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(title=post.title, content=post.content, published=post.published, owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)) :
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"[!] Error, Post with id {id} not found!")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)) :
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, (str(id), ))
    # d_post = cursor.fetchone()
    d_post = db.query(models.Post).filter_by(id=id)
    if d_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"[!] Error, Post with id {id} not found!")
    # conn.commit()

    if d_post.first().owner_id == current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"[!] Error, Not authrorized")

    d_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)) :
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *; """, (post.title, post.content, post.published, str(id)))
    # upost = cursor.fetchone()
    post_query = db.query(models.Post).filter_by(id=id)
    if post_query.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"[!] Error, Post with id {id} not found!")
    # conn.commit()
    if post_query.first().owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"[!] Error, Not authorized")
       
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()