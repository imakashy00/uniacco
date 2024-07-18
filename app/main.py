from fastapi import FastAPI, Depends, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)
from httpx import get
from schemas import Login, ResUser, Token
from utils import create_user, get_user_by_email, send_email_otp,set_otp
from auth import authenticate_user, create_access_token, get_current_user
from database import SessionLocal, engine, get_db
import models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.post("/api/register")
@limiter.limit("10/minute") 
async def register_user(user:ResUser, db:Session = Depends(get_db),status_code=status.HTTP_201_CREATED):
    db_user = get_user_by_email(db,user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        try:
            create_user(db,user)
            return {"message": "Registration successful. Please verify your email."}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong!")


@app.post("/api/request-otp")
@limiter.limit("10/minute") 
async def request_otp(request:Login, db: Session= Depends(get_db),status_code = status.HTTP_200_OK):
    db_user = get_user_by_email(db,request.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Email doesn't exits")
    else:
        try:
            otp = send_email_otp(request.email)
            set_otp(db,request,otp)
            print(f"OTP for {request.email}: {otp}")
            return { "message": "OTP sent to your email." }
        except:
            raise HTTPException(status_code=500, detail="Something went wrong!")



@app.post("/api/verify-otp")
@limiter.limit("10/minute") 
async def verify_otp(request:Token, db: Session = Depends(get_db)):
    user = authenticate_user(db,request.email,request.otp)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



