from configs.db_config import es, INDEX, SIZE
from typing import Optional, List, Dict


async def search_products(
    name: Optional[str] = None,
    description: Optional[str] = None
) -> List[Dict]:
    query_filters = []
    
    if name:
        query_filters.append({"match": {"product_name": name}})
    if description:
        query_filters.append({"match": {"product_description": description}})

    search_query = {
        "size": SIZE,
        "query": {
            "bool": {
                "must": query_filters if query_filters else {"match_all": {}}
            }
        }
    }

    response = await es.search(
        index=INDEX,
        body=search_query
    )

    return [hit["_source"] for hit in response["hits"]["hits"]]