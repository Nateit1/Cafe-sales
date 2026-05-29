"""
ShopTrack — Database Models
Matches the schema: Customer, Product, ProductCategory, CustomerOrder
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class ProductCategory(Base):
    __tablename__ = "product_category"

    category_id   = Column(Integer, primary_key=True, index=True)
    category_type = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "product"

    product_id   = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    description  = Column(String)
    category_id  = Column(Integer, ForeignKey("product_category.category_id"))
    price        = Column(Float, nullable=False)

    category = relationship("ProductCategory", back_populates="products")
    orders   = relationship("CustomerOrder", back_populates="product")


class Customer(Base):
    __tablename__ = "customer"

    customer_id  = Column(Integer, primary_key=True, index=True)
    first_name   = Column(String, nullable=False)
    last_name    = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    phone_number = Column(String)

    orders = relationship("CustomerOrder", back_populates="customer")


class CustomerOrder(Base):
    __tablename__ = "customer_order"

    order_id    = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    product_id  = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    quantity    = Column(Integer, nullable=False)
    month       = Column(String, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")
    product  = relationship("Product", back_populates="orders")
