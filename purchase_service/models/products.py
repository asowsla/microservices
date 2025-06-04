from sqlmodel import (SQLModel,
                      Text,
                      DateTime,
                      Field,
                      Relationship)
from typing import Optional
from pydantic import ConfigDict
from datetime import datetime, timezone


class ProductBase(SQLModel):
    model_config = ConfigDict(
        from_attributes=True
        )
    
    product_name: str = Field(
        max_length=100
        )
    
    product_description: str = Field(
        sa_type=Text
        )
    
    count_left: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase, table=True):
    __tablename__ = "products"

    product_id: Optional[int] = Field(default=None, primary_key=True)

    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )

    update_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )


class ProductUpdate(SQLModel):
    product_name: Optional[str] = Field(
        None,
        description="new name of product"
    )

    product_description: Optional[str] = Field(
        None,
        description="new description of product"
    )
    
    count_left: Optional[int] = Field(
        None,
        ge=0,
        description="quantity of product"
    )


class UserProduct(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True
        )
    
    product_id: int = Field(
        foreign_key="products.product_id"
        )
    
    user_id: int = Field(
        foreign_key="users.id"
        )
    
    purchase_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True)
        )
    
    status: str = Field(
        default="purchased"
        )

    product: Product = Relationship()