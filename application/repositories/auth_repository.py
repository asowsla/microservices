from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional
from application.models.user import User
from application.models.login import LoginHistory


# repository for handling authentication-related database operations
class AuthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).
                                       where(User.email == email)
                                       )
        return result.scalars().first()


    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


    async def add_login_history(self, user_id: int,
                                user_agent: str) -> LoginHistory:
        entry = LoginHistory(
            user_id=user_id,
            user_agent=user_agent
        )
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry


    async def close(self) -> None:
        await self.db.close()