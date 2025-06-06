from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from configs.db_config import get_db
from models.auth import TokenData
from models.users import User
from repositories.users import UserRepository


SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(
        password: str
) -> str:
    return pwd_context.hash(password)


async def authenticate_user(
        db: AsyncSession,
        username: str,
        password: str
) -> User | None:
    user = await UserRepository(db).get_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc
    
    user = await UserRepository(db).get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="inactive user"
        )
    return current_user