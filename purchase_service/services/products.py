from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product
from repositories.products import ProductRepository


async def get_all_products(
        db: AsyncSession
) -> List[Product]:
    repo = ProductRepository(db)
    return await repo.get_all()


async def get_product_by_id(
    db: AsyncSession, 
    product_id: int
) -> Optional[Product]:
    repo = ProductRepository(db)
    return await repo.get_by_id(product_id)


async def purchase_product_by_id(
    db: AsyncSession,
    product_id: int
) -> bool:
    repo = ProductRepository(db)
    product = await repo.get_by_id(product_id)
    
    if product is None:
        return False
        
    try:
        await repo.decrement_stock(product)
        return True
    except ValueError as e:
        return e