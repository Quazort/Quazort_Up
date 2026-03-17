from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True,min_length=2, max_length=50)]
    password: Annotated[str, StringConstraints(strip_whitespace=True,min_length=2, max_length=50)]
    email: EmailStr






class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class RefreshTokenSchema(BaseModel):
    refresh_token: str