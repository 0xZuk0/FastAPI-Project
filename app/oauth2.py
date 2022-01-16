from email.policy import default
from statistics import mode
from wsgiref import headers
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from .config import settings
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTE = settings.expire_time

def create_access_token(data : dict) :
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credential_exception) :
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id : int = payload.get("user_id")
        if id == None :
            raise credential_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError :
        raise credential_exception

def get_current_user(token : str = Depends(oauth2_schema), db : Session = Depends(database.get_db)) :

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )

    verified_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == verified_token.id).first()
    
    return user