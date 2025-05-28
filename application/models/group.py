from __future__ import annotations
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Text


# base model for Group with shared attributes
class GroupBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(
        sa_type=Text,
        description="name of the group",
    )


# database model for student groups
class Group(GroupBase, table=True):
    __tablename__: str = "groups"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="primary key identifier"
    )
    
    students: Mapped[List["Student"]] = Relationship(
        sa_relationship=relationship(back_populates="group")
    )


# scheme for creating new groups
class GroupCreate(GroupBase):
    pass


# scheme for updating existing groups
class GroupUpdate(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(
        default=None,
        sa_type=Text,
        description="updated name of the group",
    )