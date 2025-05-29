from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Text
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship


# base model containing common student attributes
class StudentBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(
        sa_type=Text,
        description="full name of the student"
    )
    
    group_id: Optional[int] = Field(
        default=None,
        foreign_key="groups.id",
        description="ID of the group this student belongs to"
    )


# database model representing a student
class Student(StudentBase, table=True):
    __tablename__: str = "students"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="primary key identifier"
    )
    
    group: Mapped[Optional["Group"]] = Relationship(
        sa_relationship=relationship(back_populates="students")
    )


# scheme for creating new students
class StudentCreate(StudentBase):
    pass


# scheme for updating existing students
class StudentUpdate(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(
        default=None,
        sa_type=Text,
        description="updated name of the student"
    )
    
    group_id: Optional[int] = Field(
        default=None,
        description="updated group ID for the student"
    )