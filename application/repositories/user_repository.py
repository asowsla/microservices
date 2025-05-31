from __future__ import annotations
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from application.models.user import User
from application.models.login import LoginHistory


# repository for user-related database operations
class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db


    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self._db.execute(select(User).
                                        where(User.email == email))
        return result.scalars().first()


    async def update_user(self, user: User) -> User:
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user


    async def get_login_history(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[LoginHistory]:

        result = await self._db.execute(
            select(LoginHistory).
            where(LoginHistory.user_id == user_id).
            order_by(LoginHistory.login_time.desc()).
            offset(skip).limit(limit)
            )
        return result.scalars().all()


    async def close(self) -> None:
        await self._db.close()