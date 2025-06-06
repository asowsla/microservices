# purchase_service

## description  
the service handles product purchases and provides access to available products

## service tasks:  
1. display all available products  
2. search products by name or description  
3. view detailed product information  
4. purchase products (reduces inventory stock)  

## module structure  

### `main.py`  
- entry point, initializes database and routes  
- postgreSQL connection setup  
- automatic table creation  

### `API/products.py`  
- API endpoints implementation:  
  - `/products` — list all products  
  - `/products/search` — search by name/description (proxies to `search_service`)  
  - `/products/{product_id}` — get product details  
  - `/purchase/{product_id}` — purchase product  

### `repositories/products.py`  
- `Product` model operations:  
  - retrieve all products  
  - get product by ID  
  - decrement product stock  

### `services/products.py`  
- bsiness logic:  
  - product listing  
  - purchase validation: stock check and quantity reduction  

### `services/search_proxy.py`  
- proxy to `search_service`:  
  - sends GET requests with `name` and `description` parameters  
  - includes authorization token  

## component relationships  
- all operations go through API routers  
- layered architecture: controller → service → repository  
- search functionality uses external `search_service`  