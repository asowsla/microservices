from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from shared.models.products import Product


class ProductRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> List[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = select(Product).where(Product.product_id == product_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def decrement_stock(self, product: Product) -> None:
        if product.count_left <= 0:
            raise ValueError("product is out of stock")
            
        product.count_left -= 1
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product