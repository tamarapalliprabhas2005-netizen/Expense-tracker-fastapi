import bcrypt
import jwt
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException
from sqlalchemy.orm import session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
import models
SECREAT_KEY="change-this-secreat-token"
oauth2schema=OAuth2PasswordBearer(tokenUrl="login")

def hashed_password(password:str):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
def verify_password(password:str,hashed:str):
    return bcrypt.checkpw(password.encode(),hashed.encode())
def create_token(username:str):
    payload={
        "sub":username,
        "exp":datetime.utcnow()+timedelta(hours=2)
    }
    return jwt.encode(payload,SECREAT_KEY,algorithm="HS256")
def get_user(token:str =Depends(oauth2schema),db:session=Depends(get_db)):
    try:
        username=jwt.decode(token,SECREAT_KEY,algorithms=["HS256"])["sub"]
    except:
        raise HTTPException(status_code=401,details="invalid or expire token")

    user=db.query(models.user).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=401,detail="user not found")
    return user