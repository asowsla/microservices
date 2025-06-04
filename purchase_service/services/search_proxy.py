import httpx
from typing import List, Dict, Optional
from http import HTTPStatus
from fastapi import HTTPException
from configs.db_config import SEARCH_SERVICE_URL


async def search_products_proxy(
    name: Optional[str] = None, 
    description: Optional[str] = None
) -> List[Dict]:
    if not name and not description:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="at least one parameter must match"
        )

    params = {}
    if name:
        params["name"] = name
    if description:
        params["description"] = description

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(SEARCH_SERVICE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="bad request"
        ) from exc
    
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="BAD_GATEWAY"
        ) from exc