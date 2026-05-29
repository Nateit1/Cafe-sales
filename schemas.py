"""
ShopTrack — Pydantic Schemas
Request and response validation for all endpoints
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Product Category ──────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    category_type: str

class CategoryResponse(BaseModel):
    category_id:   int
    category_type: str

    class Config:
        from_attributes = True


# ── Product ───────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    product_name: str
    description:  Optional[str] = None
    category_id:  int
    price:        float

class ProductResponse(BaseModel):
    product_id:   int
    product_name: str
    description:  Optional[str]
    category_id:  int
    price:        float

    class Config:
        from_attributes = True


# ── Customer ──────────────────────────────────────────────────────────────────

class CustomerCreate(BaseModel):
    first_name:   str
    last_name:    str
    email:        EmailStr
    phone_number: Optional[str] = None

class CustomerResponse(BaseModel):
    customer_id:  int
    first_name:   str
    last_name:    str
    email:        str
    phone_number: Optional[str]

    class Config:
        from_attributes = True


# ── Order ─────────────────────────────────────────────────────────────────────

class OrderCreate(BaseModel):
    customer_id: int
    product_id:  int
    quantity:    int
    month:       str

class OrderResponse(BaseModel):
    order_id:    int
    customer_id: int
    product_id:  int
    quantity:    int
    month:       str
    created_at:  datetime

    class Config:
        from_attributes = True


# ── Revenue ───────────────────────────────────────────────────────────────────

class RevenueResponse(BaseModel):
    total_orders:  int
    total_revenue: float
