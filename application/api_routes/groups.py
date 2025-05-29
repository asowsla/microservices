from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from http import HTTPStatus
from application.core.db_config import get_db
from application.models.group import Group, GroupCreate
from application.models.student import Student
from application.repositories.group_repository import GroupRepository
from application.repositories.student_repository import StudentRepository


router = APIRouter(prefix="/groups", tags=["groups"])


# data model for student-group operations
class StudentGroupAction(BaseModel):
    student_id: int

# create a new student group
@router.post("/", response_model=Group, status_code=HTTPStatus.CREATED)
async def create_group(
    group: GroupCreate, 
    db: AsyncSession = Depends(get_db)
) -> Group:
    repo = GroupRepository(db)
    return await repo.create_group(group.model_dump())


# get a specific group by ID
@router.get("/{group_id}", response_model=Group)
async def get_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
) -> Group:
    repo = GroupRepository(db)
    group = await repo.get_group(group_id)
    
    if not group:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="group is not found"
        )
    return group


# list all groups with pagination
@router.get("/", response_model=List[Group])
async def list_groups(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
) -> List[Group]:
    repo = GroupRepository(db)
    return await repo.get_all_groups(skip, limit)


# delete a group if it has no students
@router.delete("/{group_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
) -> None:
    group_repo = GroupRepository(db)
    group = await group_repo.get_group(group_id)

    if not group:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="group is not found"
        )

    if await group_repo.get_students_count(group_id) > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="unable to delete group with students"
        )

    await group_repo.delete_group(group)


# add a student to the specified group
@router.post("/{group_id}/students", response_model=Student)
async def add_student(
    group_id: int,
    student_data: StudentGroupAction,
    db: AsyncSession = Depends(get_db)
) -> Student:
    group_repo = GroupRepository(db)
    student_repo = StudentRepository(db)
    
    group = await group_repo.get_group(group_id)
    if not group:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="group is not found"
        )

    student = await student_repo.get_student(student_data.student_id)
    if not student:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="student is not found"
        )

    if student.group_id == group_id:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="student is already in group"
        )

    student.group_id = group_id
    db.add(student)
    await db.commit()
    await db.refresh(student)
    
    return student


# remove a student from the specified group
@router.delete("/{group_id}/students/{student_id}", 
               status_code=HTTPStatus.NO_CONTENT)
async def remove_student(
    group_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    group_repo = GroupRepository(db)
    student_repo = StudentRepository(db)
    
    group = await group_repo.get_group(group_id)
    if not group:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Group not found"
        )

    student = await student_repo.get_student(student_id)
    if not student:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Student not found"
        )

    if student.group_id != group_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Student not in group"
        )

    student.group_id = None
    db.add(student)
    await db.commit()