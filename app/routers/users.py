from fastapi import Depends, status, HTTPException, APIRouter
from starlette.routing import Router
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) : 
    user = models.User(email=user.email, password=utils.get_password_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)) :
    user = db.query(models.User).filter_by(id=id).first()
    if user == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"[!] Error, User with id {id} not found!")
    return user