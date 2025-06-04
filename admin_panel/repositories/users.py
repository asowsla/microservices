from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from typing import Optional


class UserRepository:
    def __init__(
            self,
            db: AsyncSession
) -> None:
        self.db = db


    async def get_by_username(
            self, 
            username: str
) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()


    async def get_by_email(
            self,
            email: str
) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()


    async def create(
            self,
            user_data: dict
) -> User:
        user = User(**user_data)
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user