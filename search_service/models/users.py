from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="primary key identifier"
    )
    
    username: str = Field(
        index=True,
        unique=True,
        min_length=3,
        max_length=50,
        description="unique username"
    )
    
    email: EmailStr = Field(
        index=True,
        unique=True,
        description="valid email address"
    )
    
    hashed_password: str = Field(
        description="hashed password (BCrypt)"
    )
    
    disabled: bool = Field(
        default=False,
        description="whether the user account is disabled or not"
    )