from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from application.models.user import User
from application.core.config import SETTINGS
from application.core.db_config import get_db_session, get_redis
from application.authentification.utilities import (decode_jwt, 
                                                    encode_jwt, 
                                                    validate_password)


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(email: str) -> str:
    return encode_jwt(
        payload={
            "sub": email,
            "type": "access"
        },
        expire_minutes=SETTINGS.JWT.access_token_expire_minutes
    )


# refresh JWT token
def create_refresh_token(email: str) -> str:
    return encode_jwt(
        payload={
            "sub": email,
            "type": "refresh"
        },
        expire_timedelta=timedelta(days=SETTINGS.JWT.refresh_token_expire_days)
    )


# authentication of user with email and password
async def validate_auth_user(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> User:
    invalid_credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    inactive_user_exc = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user"
    )

    user = await db.scalar(select(User).where(User.email == form_data.username))
    
    if not user or not validate_password(
        password=form_data.password,
        hashed_password=user.hashed_password
    ):
        raise invalid_credentials_exc

    if not user.is_active:
        raise inactive_user_exc

    return user


# decoding and validating JWT token
async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        return decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from e


# get current authenticated user from token payload
async def get_current_auth_user(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    payload: dict = Depends(get_current_token_payload),
) -> User:
    if email := payload.get("sub"):
        if user := await db.scalar(select(User).where(User.email == email)):
            return user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user


# redis blacklist
async def add_to_redis_blacklist(
    token: str, 
    exp_timestamp: int, 
    redis: Annotated[Redis, Depends(get_redis)]
) -> None:
    current_time = datetime.now(timezone.utc).timestamp()

    if ttl := int(exp_timestamp - current_time) > 0:
        await redis.set(token, "revoked", ex=ttl)