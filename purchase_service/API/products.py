from http import HTTPStatus
from typing import Annotated
from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Query,
                     Request)
from typing import Annotated, Optional
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_config import get_db
from models.products import Product
from models.users import User
from models.security import get_current_user
from services.search_proxy import search_products_proxy
from services.products import (get_all_products,
                               get_product_by_id,
                               purchase_product_by_id)


router = APIRouter(prefix="/products", tags=["Products"])
security = HTTPBearer()


@router.get("/", response_model=list[Product])
async def list_products(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Product]:
    return await get_all_products(db)


@router.get("/search", response_model=dict)
async def search_products(
    request: Request,  
    name: Optional[str] = Query(default=None),
    description: Optional[str] = Query(default=None),
    current_user: User = Depends(get_current_user)
) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="authorization header required"
        )

    results = await search_products_proxy(
        name=name,
        description=description,
        token=auth_header
    )
    
    return {
        "results": results,
        "user": current_user.username
    }


@router.get("/{product_id}", response_model=Product)
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int 
) -> Product:
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="product not found"
        )
    return product


@router.post("/purchase/{product_id}")
async def purchase_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int,
    current_user: User = Depends(get_current_user)  
)-> dict:
    success = await purchase_product_by_id(db, product_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="product is out of stock"
        )
    
    return {
        "status": "Purchase successful",
        "product_id": product_id,
        "user": current_user.username
    }