from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import models, schemas
from utils import get_user_by_email
from database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY: str = "89b6b82cd5c52490cacb6d9e869ea2f1a7b02f770647a12cb438e95c33d7d66f"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 25


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, email: str, sent_otp:str):
    user = get_user_by_email(db, email)
    if user:
        otp_string = user.otp
        mins, otp = otp_string.split('-')
        if datetime.now().minute <= int(mins): 
            print(datetime.now().minute,mins)           
            if otp == sent_otp:  
                return user
            raise HTTPException(status_code=422, detail="Invalid OTP")
        else:
            raise HTTPException(status_code=422, detail="OTP expired")
    else:
        raise HTTPException(status_code=404, detail="Email doesn't exist")

        

def create_access_token(data: dict) ->str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email


