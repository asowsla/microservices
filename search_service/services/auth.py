from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from models.security import (get_password_hash,
                             create_access_token,
                             authenticate_user)
from configs.config import ACCESS_TOKEN_EXPIRE_MINUTES
from repositories.users import UserRepository
from typing import Dict, Optional


async def register_user(
        db: AsyncSession,
        user_data: dict
) -> Dict:
    user_repo = UserRepository(db)
    
    if await user_repo.get_by_username(user_data["username"]):
        raise ValueError("username already registered")
    
    if await user_repo.get_by_email(user_data["email"]):
        raise ValueError("email already registered")
    
    hashed_password = get_password_hash(user_data["password"])
    user_data["hashed_password"] = hashed_password
    del user_data["password"]
    
    return await user_repo.create(user_data)


async def login_user(
        db: AsyncSession,
        username: str,
        password: str
) -> Optional[Dict]:
    user = await authenticate_user(db, username, password)
    if not user:
        return None
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }