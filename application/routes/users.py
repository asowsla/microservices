from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from http import HTTPStatus
from datetime import datetime
from application.models.user import User, UserUpdate
from application.models.login import LoginHistory
from application.core.db_config import get_db_session
from application.authentification.utilities import hash_password
from application.core.securities import (get_current_active_auth_user, 
                                         get_current_token_payload)
from application.repositories.user_repository import UserRepository



# config of router
router = APIRouter(prefix="/user", tags=["user"], responses={
    HTTPStatus.UNAUTHORIZED: {"description": "Invalid or missing credentials"},
    HTTPStatus.FORBIDDEN: {"description": "Insufficient permissions"}
    }
)


# update of authenticated user's information
@router.put("/update", response_model=User, status_code=HTTPStatus.OK, responses={
    HTTPStatus.BAD_REQUEST: {"description": "Email already registered"}
    }
)

async def update_user_data(
    update_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_active_auth_user)]
) -> User:
    repo = UserRepository(db)

    if update_data.email and update_data.email != current_user.email:
        if await repo.get_user_by_email(update_data.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="email already registered"
            )
        current_user.email = update_data.email

    if update_data.password:
        current_user.hashed_password = hash_password(update_data.password)

    return await repo.update_user(current_user)



# retrieving authenticated user's login history
@router.get("/history", response_model=List[LoginHistory], status_code=HTTPStatus.OK,
            summary="get user login history",
            description="retrieves paginated login history for the authenticated user"
            )

async def get_login_history(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_active_auth_user)],
    skip: int = 0,
    limit: int = 100,
) -> List[LoginHistory]:
    repo = UserRepository(db)
    return await repo.get_login_history(user_id=current_user.id,
                                        skip=skip,
                                        limit=limit
                                        )


# retrieving information about authenticated user
@router.get("/me", response_model=dict, status_code=HTTPStatus.OK, 
            summary="get current user info",
            description="returns basic information about the authenticated user"
            )

async def get_current_user_info(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[User, Depends(get_current_active_auth_user)]
) -> dict:
    return {
        "email": user.email,
        "is_active": user.is_active,
        "logged_in_at": datetime.fromtimestamp(
            payload.get("iat") if payload.get("iat") else None
            )
    }