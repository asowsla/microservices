from datetime import datetime as dt
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from shared.models.products import Product


async def extract_updated_products(
    session: AsyncSession, 
    last_update_time: dt
) -> List[Product]:
    result = await session.execute(
        select(Product).where(Product.update_time > last_update_time)
    )
    
    return result.scalars().all()