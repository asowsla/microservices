# search_s_ervice

## description  
the service provides an interface for product search in Elasticsearch, enabling full-text search across `product_name` and `product_description` fields.

## service tasks:  
1. support name and description search functionality  
2. index the `Product` model structure in Elasticsearch during startup  
3. implement JWT token-based security  

## module structure  

### `main.py`  
- entry point, initializes Elasticsearch connection and API routes  
- executes `ensure_index_exists()` on startup to create the search index  

### `API/search.py`  
- search API implementation:  
  - `/search` endpoint accepting `name` and `description` parameters  
  - constructs and executes Elasticsearch queries  

### `services/index_init.py`  
- elasticsearch index management:  
  - creates the index with proper mappings if non-existent  
  - defines schema based on the `Product` model structure  

### `services/search.py`  
- elasticsearch query operations:  
  - builds `match` queries for `product_name` and `product_description` fields  
  - handles search result processing  

## component relationships  
- all search operations are executed through Elasticsearch  
- required indexes are automatically created during service initialization  
- API routes delegate to corresponding service layer methods  