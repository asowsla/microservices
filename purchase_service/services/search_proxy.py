import httpx
from http import HTTPStatus
from fastapi import HTTPException
from typing import Optional
from configs.db_config import SEARCH_SERVICE_URL


async def search_products_proxy(
    name: Optional[str] = None,
    description: Optional[str] = None,
    token: Optional[str] = None
) -> list[dict]:
    if not any([name, description]):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="at least one search parameter has to match"
        )

    params, headers = ({}, {})
    if name:
        params["name"] = name
    if description:
        params["description"] = description
    if token:
        headers["Authorization"] = token 
    

    params = {
        key: value 
        for key, value in [
            ("name", name),
            ("description", description)
        ]
        if value is not None
    }
    
    headers = {"Authorization": token} if token else {}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                SEARCH_SERVICE_URL,
                params=params,
                headers=headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f"search service unavailable: {str(error)}"
        ) from error