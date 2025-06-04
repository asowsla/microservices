from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product, UserProduct
from repositories.products import ProductRepository
from typing import Optional
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload


async def get_all_products(
        db: AsyncSession
) -> List[Product]:
    return await ProductRepository(db).get_all()


async def get_product_by_id(
        db: AsyncSession,
        product_id: int
) -> Optional[Product]:
    return await ProductRepository(db).get_by_id(product_id)


async def purchase_product_by_id(
        db: AsyncSession,
        product_id: int,
        user_id: int
) -> bool:
    repo = ProductRepository(db)
    product = await repo.get_by_id(product_id)
    
    if not product or product.count_left <= 0:
        return False
    
    await repo.decrement_stock(product)
    
    user_product = UserProduct(
        product_id=product_id,
        user_id=user_id,
        status="purchased"
    )
    db.add(user_product)
    await db.commit()
    
    return True


async def return_product_by_id(
        db: AsyncSession,
        product_id: int,
        user_id: int
) -> bool:
    repo = ProductRepository(db)
    product = await repo.get_by_id(product_id)
    
    stmt = await db.execute(
        select(UserProduct).where(
            UserProduct.product_id == product_id,
            UserProduct.user_id == user_id,
            UserProduct.status == "purchased"
        )
    )

    user_product = stmt.scalar_one_or_none()
    
    if not user_product:
        return False
    
    await ProductRepository(db).increment_stock(product)
    
    user_product.status = "returned"
    await db.commit()
    return True


async def get_user_products(
        db: AsyncSession,
        user_id: int
) -> List[UserProduct]:
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="user id is required"
        )
    
    stmt = select(UserProduct).where(UserProduct.user_id == user_id)
    selectinload(UserProduct.product)

    result = await db.execute(stmt)
    return result.scalars().all()