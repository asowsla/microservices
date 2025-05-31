from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from shared.core.db_config import get_db
from shared.models.products import Product
from services.search_proxy import search_products_proxy
from services.products import (
    get_all_products, 
    get_product_by_id, 
    purchase_product_by_id
)


router = APIRouter(prefix="/products", tags=["Products"])

NOT_FOUND = HTTPStatus.NOT_FOUND
BAD_REQUEST = HTTPStatus.BAD_REQUEST
BAD_GATEWAY = HTTPStatus.BAD_GATEWAY


# retrieves a list of all available products
@router.get("/", response_model=list[Product], summary="listing all products")
async def list_products(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Product]:
    return await get_all_products(db)


# searching products by name or description using ElasticSearch
@router.get("/search", summary="search products")
async def search_products(
    name: Annotated[str | None, 
                    Query(description="Product name filter")] = None,
    description: Annotated[str | None, 
                           Query(description="Product description filter")] = None
) -> list[Product]:
    try:
        return await search_products_proxy(name, description)
    except ConnectionError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=BAD_GATEWAY
        )


@router.get("/{product_id}", response_model=Product, 
            summary="get product details by ID",
            responses={HTTPStatus.NOT_FOUND: {"description": NOT_FOUND}}
    )
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
) -> Product:
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND
        )
    return product


@router.post("/purchase/{product_id}", summary="purchase product by ID",
             responses={HTTPStatus.BAD_REQUEST: {"description": BAD_REQUEST}}
    )
async def purchase_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
) -> dict[str, str | int]:
    success = await purchase_product_by_id(db, product_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=BAD_REQUEST
        )
    return {"status": "successfully purchased", "product_id": product_id}