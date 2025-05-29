from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from application.models.group import Group
from application.models.student import Student


# repository for handling database operations for Groups
class GroupRepository:
    
    # initialize repository with database session
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    # create a new group
    async def create_group(self, group_data: dict) -> Group:
        group = Group(**group_data)
        self.db.add(group)
        await self.db.commit()
        await self.db.refresh(group)
        return group


    # retrieve a group by ID
    async def get_group(self, group_id: int) -> Optional[Group]:
        result = await self.db.execute(select(Group)
                                       .where(Group.id == group_id)
        )
        return result.scalars().first()


    # retrieve all groups with pagination
    async def get_all_groups(self, 
                             skip: int = 0, 
                             limit: int = 100
                             ) -> List[Group]:
        result = await self.db.execute(select(Group)
                                       .offset(skip)
                                       .limit(limit)
                                       .order_by(Group.id)
        )
        return result.scalars().all()


    # delete a group.
    async def delete_group(self, group: Group) -> None:
        await self.db.delete(group)
        await self.db.commit()


    # count students in a group
    async def get_students_count(self, group_id: int) -> int:
        result = await self.db.execute(select(func.count(Student.id))
                                       .where(Student.group_id == group_id)
        )
        return result.scalar()