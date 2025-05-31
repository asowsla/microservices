from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from typing import Annotated
from shared.models.products import Product, ProductCreate, ProductUpdate
from shared.core.db_config import get_db
from services.products import create_product, update_product


router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

NOT_FOUND = HTTPStatus.NOT_FOUND


@router.post("/", response_model=Product)
async def create_product_endpoint(
    product: ProductCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Product:
    return await create_product(db, product)


# product update
@router.patch("/{product_id}", response_model=Product)
async def update_product_endpoint(
    product_id: int, 
    product: ProductUpdate, 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Product:
    updated_product = await update_product(db, product_id, product)
    
    if not updated_product:
        raise HTTPException(
            status_code=NOT_FOUND,
            detail="product is not found"
        )
    
    return updated_product