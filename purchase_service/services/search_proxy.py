import httpx
from http import HTTPStatus
from fastapi import HTTPException
from shared.core.db_config import SEARCH_SERVICE_URL


async def search_products_proxy(
    name: str | None = None,
    description: str | None = None,
    token: str | None = None
) -> list[dict]:
    if not name and not description:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Укажите название продукта или его описание"
        )

    params = {}
    if name:
        params["name"] = name
    if description:
        params["description"] = description

    headers = {}
    if token:
        headers["Authorization"] = token 

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(SEARCH_SERVICE_URL, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f"Search service error: {str(e)}"
        )