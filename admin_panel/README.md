# admin_Panel

## description  
the service is designed for product management in the system. It allows user registration, product management (creation and updates), and implements protection using JWT tokens.  

## service tasks:  
1. user registration and login  
2. product management (creation and updates)  
3. resource protection using OAuth2 tokens  

## module structure  

### `main.py`  
- application entry point  
- database connection initialization via `engine`  
- automatic table creation via `SQLModel`  
- integration of routes from the `API` folder  

### `API/auth.py`  
- authentication implementation  
  - `/register` — user registration  
    - checks username and email uniqueness  
    - hashes the password before saving  
  - `/token` — token generation using login and password  
    - validates credentials  
    - generates a JWT token  

### `API/products.py`  
- product management methods  
  - `/admin/products/` — create a new product  
  - `/admin/products/{product_id}` — update product information  

### `repositories/users.py`  
- interaction with the `User` model  
  - retrieving a user by username or email  
  - creating a new user  

### `services/auth.py`  
- authentication business logic:  
  - registration: uniqueness check, password hashing, database insertion  
  - authorization: token generation  

### `services/products.py`  
- product-related logic:  
  - creation and updates of database records  

## components relationships  
- all requests pass through API routers (`auth`, `products`)  
- logic is separated into layers: controller (router) → service → repository  
- authentication is secured using `OAuth2PasswordBearer`  