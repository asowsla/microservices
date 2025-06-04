from typing import List
from models.products import Product
from configs.db_config import es, INDEX


async def load_to_elasticsearch(
        products: List[Product]
) -> None:
    for product in products:
        try:
            await es.index(
                index=INDEX,
                id=str(product.product_id),
                document=product.model_dump(),
                refresh=True
            )
        except Exception as error:
            raise RuntimeError(
                f"failed to index product {product.product_id}: {str(error)}"
            ) from error