from typing import Union, Dict, Type, get_args, get_origin
from datetime import datetime
from sqlmodel import SQLModel
from elasticsearch import AsyncElasticsearch
from shared.models.products import Product


PYDANTIC_TO_ES_TYPE_MAPPING = {
    str: {"type": "text"},
    int: {"type": "integer"},
    float: {"type": "float"},
    bool: {"type": "boolean"},
    datetime: {"type": "date"},
}


# extracting the underlying field type
def get_underlying_field_type(field_type: type) -> type:
    if get_origin(field_type) is Union:
        field_type = [arg for arg in get_args(field_type) 
                      if arg is not type(None)][0]
    
    return getattr(field_type, '__origin__', field_type)


# generating Elasticsearch mappings from a SQLModel class
def generate_es_mappings(model: Type[SQLModel]) -> Dict:
    properties = {}

    for field_name, field in model.model_fields.items():
        field_type = get_underlying_field_type(field.annotation)

        es_type = PYDANTIC_TO_ES_TYPE_MAPPING.get(field_type,
                                                  {"type": "text"})
        properties[field_name] = es_type

    return {"mappings": {"properties": properties}}


async def ensure_index_exists(
        es: AsyncElasticsearch, 
        index: str, 
        model: Type[SQLModel] = Product
) -> None:
    if not await es.indices.exists(index=index):
        await es.indices.create(
            index=index, 
            body=generate_es_mappings(model)
        )