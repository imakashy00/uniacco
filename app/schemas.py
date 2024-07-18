from pydantic import BaseModel, EmailStr

class ResUser(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class Login(BaseModel):

    email: EmailStr
    
    class Config:
        from_attributes = True
        

class Token(BaseModel):
    email:EmailStr
    otp: str

    class Config:
        from_attributes = True