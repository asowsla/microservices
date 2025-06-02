from fastapi import APIRouter, HTTPException, Query, Depends
from http import HTTPStatus
from services.search import search_products
from shared.models.users import User
from shared.models.security import get_current_user


router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def search(
    name: str | None = Query(None),
    description: str | None = Query(None),
    current_user: User = Depends(get_current_user)
):
    if not name and not description:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нужно указать name или description"
        )

    try:
        results = await search_products(name, description)
        return {
            "results": results,
            "user": current_user.username
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f"Search error: {str(e)}"
        )