from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from typing import Annotated
from http import HTTPStatus
from jwt.exceptions import InvalidTokenError
from application.models.user import User, UserCreate
from application.models.login import LoginHistory
from application.core.db_config import get_db_session, get_redis
from application.core.securities import (create_access_token,
                                         create_refresh_token,
                                         validate_auth_user,
                                         add_to_redis_blacklist
                                         )
from application.authentification.utilities import hash_password, decode_jwt
from application.repositories.auth_repository import AuthRepository



#config of router
router = APIRouter(prefix="/auth", tags=["authentication"], responses={
    HTTPStatus.UNAUTHORIZED: {"description": "invalid credentials"},
    HTTPStatus.FORBIDDEN: {"description": "operation not permitted"}
    }
)
security = HTTPBearer()



# new user account
@router.post("/register", response_model=User, status_code=HTTPStatus.CREATED, responses={
    HTTPStatus.BAD_REQUEST: {"description": "email already registered"}
    }
)

async def register_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db_session)]
) -> User:
    repo = AuthRepository(db)
    
    if await repo.get_user_by_email(user_data.email):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)

    return await repo.create_user(new_user)



# authentication of user and generation of access tokens
@router.post("/login", response_model=dict, status_code=HTTPStatus.OK, responses={
    HTTPStatus.UNAUTHORIZED: {"description": "Invalid credentials"},
    HTTPStatus.FORBIDDEN: {"description": "Inactive account"}
    }
)

async def login_user(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    user: User = Depends(validate_auth_user)
) -> dict:
    repo = AuthRepository(db)

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    login_entry = LoginHistory(
        user_id=user.id,
        user_agent=user.email or "unknown"
    )

    await repo.add_login_history(login_entry)

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
            }



# generation of new access token using a valid refresh token
@router.post("/refresh", response_model=dict, status_code=HTTPStatus.OK, responses={
    HTTPStatus.UNAUTHORIZED: {"description": "invalid or revoked token"}
    }
)

async def refresh_access_token(
    refresh_token: str,
    redis: Annotated[Redis, Depends(get_redis)]
) -> dict:
    try:
        if await redis.exists(refresh_token):
            raise InvalidTokenError("token revoked")
        
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise InvalidTokenError("invalid token type")
        
        new_access_token = create_access_token(payload["sub"])

        await add_to_redis_blacklist(refresh_token, payload["exp"], redis)

        return {"access_token": new_access_token}

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"})



# logout in case if invalide refresh token
@router.post("/logout", status_code=HTTPStatus.OK, responses={
    HTTPStatus.UNAUTHORIZED: {"description": "invalid or revoked token"}
    }
)

async def logout_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    redis: Annotated[Redis, Depends(get_redis)]
) -> dict:
    token = credentials.credentials

    if await redis.exists(token):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="token is already revoked"
        )

    payload = decode_jwt(token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="invalid token type"
        )

    await add_to_redis_blacklist(token, payload["exp"], redis)

    return {"detail": "successful logging out"}