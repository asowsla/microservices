from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from http import HTTPStatus
from application.core.db_config import get_db
from application.models.student import Student, StudentCreate, StudentUpdate
from application.repositories.student_repository import StudentRepository
from application.repositories.group_repository import GroupRepository


router = APIRouter(prefix="/students", tags=["students"])


# data model for student transfer between groups
class TransferRequest(BaseModel):
    from_group_id: int
    to_group_id: int


# create a new student
@router.post("/", response_model=Student, status_code=HTTPStatus.CREATED)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
) -> Student:
    repo = StudentRepository(db)
    group_repo = GroupRepository(db)

    if student.group_id is not None:
        if not await group_repo.get_group(student.group_id):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="invalid group ID"
            )

    return await repo.create_student(student)


# get student by ID
@router.get("/{student_id}", response_model=Student)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
) -> Student:
    repo = StudentRepository(db)
    student = await repo.get_student(student_id)
    
    if not student:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="student is not found"
        )
    return student


# list students with optional group filtering
@router.get("/", response_model=List[Student])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    group_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
) -> List[Student]:
    repo = StudentRepository(db)
    return await repo.get_students(skip, limit, group_id)


# update student information
@router.patch("/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    db: AsyncSession = Depends(get_db)
) -> Student:
    repo = StudentRepository(db)
    group_repo = GroupRepository(db)

    update_data = student.model_dump(exclude_unset=True)

    if "group_id" in update_data and update_data["group_id"] is not None:
        if not await group_repo.get_group(update_data["group_id"]):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="invalid group ID"
            )

    updated_student = await repo.update_student(student_id, update_data)

    if not updated_student:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="student is not found"
        )
    return updated_student


# delete student by ID
@router.delete("/{student_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    repo = StudentRepository(db)

    if not await repo.delete_student(student_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="student is not found"
        )


# transfer student to another group
@router.post("/{student_id}/transfer", response_model=Student)
async def transfer_student(
    student_id: int,
    transfer_data: TransferRequest,
    db: AsyncSession = Depends(get_db)
) -> Student:
    student_repo = StudentRepository(db)
    group_repo = GroupRepository(db)

    student = await student_repo.get_student(student_id)

    if not student:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="student is not found"
        )

    if student.group_id != transfer_data.from_group_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="student is not in source group"
        )

    if not await group_repo.get_group(transfer_data.to_group_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="target group is not found"
        )

    if student.group_id == transfer_data.to_group_id:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="student is already in target group"
        )

    return await student_repo.transfer_student(student, 
                                               transfer_data.to_group_id)