from __future__ import annotations
from typing import Optional, List
from pydantic import ConfigDict, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Text, Boolean
from sqlalchemy.orm import Mapped, relationship


# model containing user fields
class UserBase(SQLModel):    
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )
    
    email: EmailStr = Field(
        index=True,
        unique=True,
        sa_type=Text,
        description="user's unique email address"
    )


# model representing a user
class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = {"comment": "registered user accounts"}
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="primary key identifier"
    )
    
    hashed_password: str = Field(
        sa_type=Text,
        description="BCrypt hashed password",
        exclude=True
    )
    
    is_active: bool = Field(
        default=True,
        sa_type=Boolean,
        description="whether the account is active or not"
    )
    
    login_history: Mapped[List["LoginHistory"]] = Relationship(
        sa_relationship=relationship(
            back_populates="user",
            lazy="selectin",
            cascade="all, delete-orphan"
            )
        )


class UserCreate(UserBase):
    password: str = Field(
        min_length=4,
        max_length=64,
        description="password is set be from 4 to 64 characters"
    )
    

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(c.isupper() for c in value):
            raise ValueError("password must contain uppercase letters")
        if not any(c.isdigit() for c in value):
            raise ValueError("password must contain numbers")
        return value


class UserUpdate(SQLModel):    
    email: Optional[EmailStr] = Field(
        default=None,
        description="new email address"
    )
    
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=64,
        description="new password is set to be from 8 to 64 characters"
    )
    
    is_active: Optional[bool] = Field(
        default=None,
        description="set account active status"
    )