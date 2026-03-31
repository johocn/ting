from pydantic import BaseModel
from typing import Optional

class ProductCategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    sort_order: Optional[int] = 0
    is_active: Optional[bool] = True

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    category_id: Optional[int] = None
    points_required: int
    stock_quantity: Optional[int] = 0
    max_exchange_per_user: Optional[int] = 0
    is_virtual: Optional[bool] = False
    validity_period_days: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    points_required: Optional[int] = None
    stock_quantity: Optional[int] = None
    max_exchange_per_user: Optional[int] = None
    is_active: Optional[bool] = None
    is_virtual: Optional[bool] = None
    validity_period_days: Optional[int] = None

class ExchangeRequest(BaseModel):
    product_id: int
    quantity: Optional[int] = 1

class ExchangeRecordResponse(BaseModel):
    id: int
    product_name: str
    points_deducted: int
    quantity: int
    exchange_code: str
    exchange_time: str
    status: str
    validity_start_date: str
    validity_end_date: str

class StoreBase(BaseModel):
    name: str
    address: Optional[str] = ""
    phone: Optional[str] = ""
    manager_user_id: Optional[int] = None
    is_active: Optional[bool] = True

class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    manager_user_id: Optional[int] = None
    is_active: Optional[bool] = None
