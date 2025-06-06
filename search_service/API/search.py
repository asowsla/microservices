from fastapi import APIRouter, HTTPException, Query, Depends
from http import HTTPStatus
from services.search import search_products
from models.users import User
from models.security import get_current_user
from typing import Optional


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=dict)
async def search(
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
) -> dict:
    if not any([name, description]):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="at least one search parameter has to match"
        )

    try:
        results = await search_products(name=name, description=description)
        return {
            "results": results,
            "user": current_user.username
        }
        
    except Exception as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f"Search service error: {str(error)}"
        ) from error