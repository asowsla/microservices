from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from configs.db_config import get_db
from models.auth import UserCreate, Token
from services.auth import register_user, login_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Token:
    try:
        await register_user(db, user_data.model_dump())
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error)
        ) from error
    
    return await login_user(
        db=db,
        username=user_data.username,
        password=user_data.password
    )

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    token = await login_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token