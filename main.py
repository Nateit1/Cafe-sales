"""
ShopTrack — E-Commerce Backend API
REST API for managing products, customers, categories, and orders.
Built with FastAPI + PostgreSQL + SQLAlchemy.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import models
import schemas
from database import engine, get_db

# ── Create Tables ─────────────────────────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ShopTrack API",
    description="E-Commerce Backend — manage products, customers, and orders.",
    version="1.0.0"
)

# ── Root ──────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "Welcome to ShopTrack API",
        "docs":    "/docs",
        "version": "1.0.0"
    }

# ── Categories ────────────────────────────────────────────────────────────────

@app.get("/categories", response_model=List[schemas.CategoryResponse], tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    """List all product categories."""
    return db.query(models.ProductCategory).all()

@app.post("/categories", response_model=schemas.CategoryResponse, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Add a new product category."""
    db_category = models.ProductCategory(category_type=category.category_type)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# ── Products ──────────────────────────────────────────────────────────────────

@app.get("/products", response_model=List[schemas.ProductResponse], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    """List all products."""
    return db.query(models.Product).all()

@app.get("/products/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID."""
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

@app.post("/products", response_model=schemas.ProductResponse, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product."""
    category = db.query(models.ProductCategory).filter(
        models.ProductCategory.category_id == product.category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product by ID."""
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(product)
    db.commit()
    return {"message": f"Product {product_id} deleted."}

# ── Customers ─────────────────────────────────────────────────────────────────

@app.get("/customers", response_model=List[schemas.CustomerResponse], tags=["Customers"])
def get_customers(db: Session = Depends(get_db)):
    """List all customers."""
    return db.query(models.Customer).all()

@app.get("/customers/{customer_id}", response_model=schemas.CustomerResponse, tags=["Customers"])
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a single customer by ID."""
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer

@app.post("/customers", response_model=schemas.CustomerResponse, tags=["Customers"])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """Add a new customer."""
    existing = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/customers/{customer_id}", tags=["Customers"])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer by ID."""
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    db.delete(customer)
    db.commit()
    return {"message": f"Customer {customer_id} deleted."}

# ── Orders ────────────────────────────────────────────────────────────────────

@app.get("/orders", response_model=List[schemas.OrderResponse], tags=["Orders"])
def get_orders(db: Session = Depends(get_db)):
    """List all orders."""
    return db.query(models.CustomerOrder).all()

@app.get("/orders/customer/{customer_id}", response_model=List[schemas.OrderResponse], tags=["Orders"])
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    """Get all orders for a specific customer."""
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return db.query(models.CustomerOrder).filter(
        models.CustomerOrder.customer_id == customer_id
    ).all()

@app.post("/orders", response_model=schemas.OrderResponse, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Place a new order."""
    customer = db.query(models.Customer).filter(models.Customer.customer_id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    product = db.query(models.Product).filter(models.Product.product_id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    db_order = models.CustomerOrder(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# ── Revenue Report ────────────────────────────────────────────────────────────

@app.get("/revenue", response_model=schemas.RevenueResponse, tags=["Reports"])
def get_revenue(db: Session = Depends(get_db)):
    """Get total revenue and order count across all orders."""
    orders = db.query(models.CustomerOrder).all()
    total_revenue = sum(
        o.quantity * db.query(models.Product).filter(
            models.Product.product_id == o.product_id
        ).first().price
        for o in orders
    )
    return {
        "total_orders":  len(orders),
        "total_revenue": round(total_revenue, 2)
    }
