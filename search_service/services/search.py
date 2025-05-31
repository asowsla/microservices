from typing import List, Optional
from shared.core.db_config import es, INDEX, SIZE


# search products in Elasticsearch by name and/or description
async def search_products(
    name: Optional[str] = None, 
    description: Optional[str] = None
) -> List[dict]:
    query = build_search_query(name, description)
    response = await execute_es_search(query)
    return extract_search_results(response)


def build_search_query(name: Optional[str], description: Optional[str]) -> dict:
    must_clauses = []

    if name:
        must_clauses.append({"match": {"product_name": name}})
    if description:
        must_clauses.append({"match": {"product_description": description}})

    return {"size": SIZE, "query": {"bool":
                                    {"must": must_clauses if must_clauses else []}
                                }
                            }


# execute search request in Elasticsearch
async def execute_es_search(query: dict) -> dict:
    return await es.search(index=INDEX, body=query)


# extract hits from Elasticsearch response
def extract_search_results(response: dict) -> List[dict]:
    return [hit["_source"] for hit in response["hits"]["hits"]]