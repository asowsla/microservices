from typing import Optional, List, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.models.student import Student
from application.models.group import Group


# repository for handling all database operations related to Students
class StudentRepository:


    # initialize the repository with a database session
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    # create a new student record
    async def create_student(self, student_data: Dict) -> Student:
        student = Student(**student_data)
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student


    # retrieve a student by their ID
    async def get_student(self, student_id: int) -> Optional[Student]:
        result = await self.db.execute(select(Student)
                                       .where(Student.id == student_id)
        )
        return result.scalars().first()


    # retrieve students with optional filtering and pagination
    async def get_all_students(self,
                               skip: int = 0,
                               limit: int = 100,
                               group_id: Optional[int] = None
    ) -> List[Student]:
        query = select(Student).order_by(Student.id)
        
        if group_id is not None:
            query = query.where(Student.group_id == group_id)
            
        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()


    # update a student's attributes
    async def update_student(
        self,
        student: Student,
        update_data: Dict
    ) -> Student:
        for key, value in update_data.items():
            if hasattr(student, key):
                setattr(student, key, value)
                
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student


    # delete a student record
    async def delete_student(self, student: Student) -> None:
        await self.db.delete(student)
        await self.db.commit()


    # retrieve a group by its ID
    async def get_group(self, group_id: int) -> Optional[Group]:
        result = await self.db.execute(select(Group)
                                       .where(Group.id == group_id)
        )
        return result.scalars().first()