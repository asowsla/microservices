from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List, Optional, Dict
from services.search import search_products


router = APIRouter(prefix="/search", tags=["Search"])

BAD_REQUEST = HTTPStatus.BAD_REQUEST
BAD_GATEWAY = HTTPStatus.BAD_GATEWAY


@router.get("/", summary="Search products", 
            description="Search products by name or description", response_model=List[Dict]
    )
async def search(
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None)
) -> None:
    if not name and not description:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail=BAD_REQUEST
        )

    try:
        results = await search_products(name, description)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=BAD_GATEWAY,
            detail=BAD_GATEWAY
        )