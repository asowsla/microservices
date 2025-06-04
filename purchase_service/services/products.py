from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product
from repositories.products import ProductRepository
from typing import Optional


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
        product_id: int
) -> bool:
    repo = ProductRepository(db)
    product = await repo.get_by_id(product_id)
    
    if not product or product.count_left <= 0:
        return False
    
    await repo.decrement_stock(product)
    return True