from typing import List, Optional
from fastapi import HTTPException
from configs.db_config import es, INDEX, SIZE


# search products in Elasticsearch by name and/or description
async def search_products(
    name: Optional[str] = None, 
    description: Optional[str] = None
) -> List[dict]:
     try:
        if not any([name, description]):
            return []
            
        query = build_search_query(name, description)
        response = await execute_es_search(query)
        return extract_search_results(response)
     
     except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"bad request: {str(e)}"
        )


def build_search_query(
        name: Optional[str],
        description: Optional[str]
) -> dict:
    must_clauses = []

    if name:
        must_clauses.append({
            "match": {"product_name": {"query": name}}
            })
    if description:
        must_clauses.append({
            "match": {"product_description": {"query": description}}
        })

    return {"size": SIZE, 
            "query": {"bool": {"must": must_clauses if must_clauses else []}
                                }
                            }


async def execute_es_search(query: dict) -> dict:
    return await es.search(
        index=INDEX,
        body=query
    )


def extract_search_results(response: dict) -> List[dict]:
    return [
        {
        "name": hit["_source"]["product_name"],
        "description": hit["_source"].get("product_description", "")
    } 
    for hit in response["hits"]["hits"]
]