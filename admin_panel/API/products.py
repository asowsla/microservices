from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from typing import Annotated
from shared.models.products import Product, ProductCreate, ProductUpdate
from shared.models.users import User
from shared.core.db_config import get_db
from shared.models.security import get_current_user
from services.products import create_product, update_product


router = APIRouter(prefix="/admin/products", tags=["Admin Panel"])

@router.post("/", response_model=Product)
async def create(
    product: ProductCreate, 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user) 
):
    try:
        created_product = await create_product(db, product)
        return {
            "product": created_product,
            "created_by": current_user.username 
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Ошибка создания продукта: {str(e)}"
        )


@router.patch("/{product_id}", response_model=Product)
async def update(
    product_id: int, 
    product: ProductUpdate, 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user) 
):
    try:
        updated = await update_product(db, product_id, product)
        if not updated:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Product not found")
        
        return {
            "product": updated,
            "updated_by": current_user.username 
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Ошибка обновления продукта: {str(e)}"
        )