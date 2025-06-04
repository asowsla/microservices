from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    access_token: str = Field(
        description="JWT access token"
    )

    token_type: str = Field(
        default="bearer",
        description="token type"
    )

class TokenData(BaseModel):
    username: Optional[str] = Field(
        default=None,
        description="username extracted from token"
    )

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        description="unique username"
    )

    email: EmailStr = Field(
        description="valid email address"
    )
    
    password: str = Field(
        min_length=3,
        max_length=20,
        description="password"
    )

class UserLogin(BaseModel):
    username: str = Field(
        description="registered username"
    )

    password: str = Field(
        description="user's password"
    )