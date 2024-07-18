
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
import random, string
from datetime import datetime, timedelta

sent_otp = None

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.ResUser):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def send_email_otp(email)->str:
    sent_otp = ''.join(random.choices(string.digits, k=6))
    return sent_otp


def set_otp(db: Session, request:schemas.Login, otp:str):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        try:
            user.otp = f'{datetime.now().minute + int(timedelta(minutes=5).total_seconds()/60)}-{otp}'
            # print(user.otp)
            db.commit()
            db.refresh(user)
        except  Exception as e:
            print(e)
    else:
        raise HTTPException(status_code=404, detail="Email not found")

