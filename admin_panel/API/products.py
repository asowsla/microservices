from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from typing import Annotated
from models.products import Product, ProductCreate, ProductUpdate
from models.users import User
from configs.db_config import get_db
from models.security import get_current_user
from services.products import create_product, update_product


router = APIRouter(prefix="/admin/products", tags=["Admin Panel"])


@router.post("/", response_model=Product)
async def create_product_endpoint(
    product: ProductCreate, 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user) 
) -> dict:
    try:
        created_product = await create_product(db, product)
        return {
            "product": created_product,
            "created_by": current_user.username 
        }
    except Exception as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"product creation error: {str(error)}"
        ) from error


@router.patch("/{product_id}", response_model=Product)
async def update_product_endpoint(
    product_id: int, 
    product_data: ProductUpdate, 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user) 
) -> dict:
    try:
        product = await update_product(db, product_id, product_data)
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="product not found"
            )
        return {
            "product": product,
            "updated_by": current_user.username 
        }
    except Exception as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"product update error: {str(error)}"
        ) from error