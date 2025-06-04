from datetime import datetime as dt, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.products import (Product,
                             ProductCreate,
                             ProductUpdate)
from typing import Optional


async def create_product(
        db: AsyncSession,
        product: ProductCreate
) -> Product:
    new_product = Product(**product.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


async def update_product(
        db: AsyncSession,
        product_id: int,
        product: ProductUpdate
) -> Optional[Product]:
    result = await db.execute(
        select(Product).where(Product.product_id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        return None
    
    update_values = product.model_dump(exclude_unset=True)
    for field, value in update_values.items():
        setattr(product, field, value)
    
    product.update_time = dt.now(timezone.utc)
    
    await db.commit()
    await db.refresh(product)
    
    return product