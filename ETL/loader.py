from typing import List
from shared.models.products import Product
from shared.core.db_config import es, INDEX


# uploading products one-by-one in Elasticsearch
async def load_to_elasticsearch(products: List[Product]) -> None:
    for product in products:
        try:
            await es.index(
                index=INDEX,
                id=str(product.product_id),
                document=product.model_dump(),
                refresh=True
            )
        except Exception as e:
            raise RuntimeError(
                f"failed to index product {product.product_id}: {str(e)}"
            ) from e