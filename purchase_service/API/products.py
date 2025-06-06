from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_config import get_db
from models.products import Product
from services.search_proxy import search_products_proxy
from services.products import (get_all_products,
                               get_product_by_id,
                               purchase_product_by_id)


router = APIRouter(prefix="/products", tags=["Products"])


# retrieves a list of all available products
@router.get("/", response_model=list[Product], summary="listing all products")
async def list_products(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Product]:
    return await get_all_products(db)


# searching products by name or description using ElasticSearch
@router.get("/search", summary="search products",
            responses={HTTPStatus.BAD_GATEWAY: {"description": "bad gateway"}})
async def search_products(
    name: Annotated[str | None, Query(description="Product name filter")] = None,
    description: Annotated[str | None, Query(description="Product description filter")] = None
) -> list[Product]:
    try:
        return await search_products_proxy(name, description)
    except ConnectionError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="search service unavailable"
        )


@router.get("/{product_id}", response_model=Product, 
            summary="get product details by ID",
            responses={HTTPStatus.NOT_FOUND: {"description": "not found"}}
    )
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
) -> Product:
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="product not found"
        )
    return product


@router.post("/purchase/{product_id}", summary="purchase product by ID",
             responses={HTTPStatus.BAD_REQUEST: {"description": "bad request"}}
    )
async def purchase_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
) -> dict[str, str | int]:
    success = await purchase_product_by_id(db, product_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="purchase failed"
        )
    return {"status": "successfully purchased", "product_id": product_id}