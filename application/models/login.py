from __future__ import annotations
from datetime import datetime as dt
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Relationship, Text, DateTime
from sqlalchemy.orm import Mapped, relationship


# model for login history records
class LoginHistoryBase(SQLModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={
            dt: lambda v: v.isoformat()
        }
    )
    
    user_agent: str = Field(
        sa_type=Text,
        description="the user agent string from the login request",
        max_length=512
    )
    
    login_time: dt = Field(
        default_factory=lambda: dt.now(ZoneInfo("MSK")),
        sa_type=DateTime(timezone=True),
        description="timestamp of the login event in MSK"
    )


# tracking user login history
class LoginHistory(LoginHistoryBase, table=True):
    __tablename__ = "login_history"
    __table_args__ = {"comment": "tracks historical user login events"}
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="primary key identifier"
    )
    
    user_id: int = Field(
        foreign_key="users.id",
        description="foreign key reference to the user"
    )
    
    user: Mapped[Optional["User"]] = Relationship(
        sa_relationship=relationship(
            back_populates="login_history",
            lazy="selectin"
        )
    )