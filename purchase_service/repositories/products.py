from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product, UserProduct
from sqlalchemy.orm import selectinload


class ProductRepository:
    def __init__(
            self,
            db: AsyncSession
) -> None:
        self.db = db


    async def get_all(
            self
) -> List[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()


    async def get_by_id(
            self,
            product_id: int
) -> Optional[Product]:
        result = await self.db.execute(
            select(Product).where(Product.product_id == product_id)
        )
        return result.scalar_one_or_none()


    async def increment_stock(
            self,
            product: Product
) -> None:
        product.count_left += 1
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)    


    async def decrement_stock(
            self,
            product: Product
) -> None:
        product.count_left -= 1
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)


class UserProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_product(
            self,
            product_id: int,
            user_id: int
) -> Optional[UserProduct]:
        result = await self.db.execute(
            select(UserProduct).where(
                UserProduct.product_id == product_id,
                UserProduct.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    

    async def get_purchased_product(
            self,
            product_id: int,
            user_id: int
    ) -> Optional[UserProduct]:
        result = await self.db.execute(
            select(UserProduct).where(
                UserProduct.product_id == product_id,
                UserProduct.user_id == user_id,
                UserProduct.status == "purchased"
            )
        )
        return result.scalar_one_or_none()
    

    async def get_all_products(
            self,
            user_id: int
    ) -> List[UserProduct]:
        stmt = select(UserProduct).where(UserProduct.user_id == user_id)
        selectinload(UserProduct.product)
        result = await self.db.execute(stmt)
        return result.scalars().all()