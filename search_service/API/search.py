from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List, Optional, Dict
from services.search import search_products


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", summary="Search products", 
            description="Search products by name or description", 
            response_model=List[Dict]
        )
async def search(
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None)
) -> None:
    if not name and not description:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="name and description doesnt match"
        )

    try:
        results = await search_products(name, description)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="bad gateway"
        )