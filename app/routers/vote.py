from operator import mod
from os import stat
from statistics import mode
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models


router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)) :
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"[!] Error, Post not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == True :
        if found_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted")
        else :
            v = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(v)
            db.commit()
            return {"message" : "Vote added"}
    else :
        if not found_vote :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        else :
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message" : "Vote deleted"} 