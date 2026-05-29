# ☕ CafeSales — Database & REST API

> A full-stack database project built on a real cafe sales dataset — featuring SQL analysis in SQL Server and a REST API built with FastAPI and PostgreSQL.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=flat-square&logo=postgresql)
![SQL Server](https://img.shields.io/badge/SQL_Server-Queries-red?style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?style=flat-square)

---

## 📌 What It Does

CafeSales is a two-part database project built on a real cafe sales dataset:

1. **SQL Analysis** — Designed the database schema in SQL Server, loaded real data, and wrote queries covering ORDER BY, GROUP BY, and multi-table JOINs
2. **REST API** — Built a FastAPI backend on top of the same schema using PostgreSQL and SQLAlchemy, with full CRUD and a revenue reporting endpoint

---

## 📸 Database Diagram

<img width="847" height="577" alt="Picture1" src="https://github.com/user-attachments/assets/47934de3-8cfc-4b78-8e30-da0e414fb9f6" />


---

## 🗂️ Project Structure

```
cafe-sales/
├── main.py              ← FastAPI app with all endpoints
├── models.py            ← SQLAlchemy database models
├── schemas.py           ← Pydantic request/response validation
├── database.py          ← PostgreSQL connection
├── requirements.txt
├── .env.example
├── queries/
│   └── sales_queries.sql  ← All SQL queries with results
└── screenshots/
    ├── database-diagram.png
    ├── q1a-single-sort-desc.png
    ├── q1b-double-sort-desc.png
    ├── q1c-order-asc.png
    ├── q1d-double-sort-asc.png
    ├── q2-group-by-month.png
    ├── q3-group-by-sales-order.png
    ├── q4-join-product-category.png
    ├── q5-join-high-quantity.png
    └── q6-join-low-quantity.png
```

---

## 🗄️ Database Schema

```
ProductCategory          Product
───────────────          ──────────────────────────
category_id (PK)    ←── category_id (FK)
category_type            product_id (PK)
                         product_name
                         description
                         price

Customer                 CustomerOrder
────────────────         ──────────────────────────
customer_id (PK)    ←── customer_id (FK)
first_name               product_id (FK) ──→ Product
last_name                order_id (PK)
email (unique)           quantity
phone_number             month

                    SalesOrder
                    ──────────────────────────
                    product_id (FK) ──→ Product
                    sold_quantity
                    month
```

---

## 📊 Part 1 — SQL Analysis

All queries written and executed in SQL Server Management Studio on the live Cafe_Sales database.

### ORDER BY — Single Sort DESC
> Highest quantity orders first

<img width="1278" height="945" alt="image" src="https://github.com/user-attachments/assets/6492341d-9e3d-4a9d-bbd3-8378b39b83db" />


### ORDER BY — Double Sort DESC
> Highest quantity + month, both descending

<img width="1279" height="959" alt="image" src="https://github.com/user-attachments/assets/ec7eda73-09f8-4c85-8620-93ba517daffa" />


### ORDER BY — Single Sort ASC
> Lowest quantity orders first — C196 purchased Product 109 in Feb with quantity 10

<img width="1279" height="959" alt="image" src="https://github.com/user-attachments/assets/1a11f32f-8873-49c3-a28c-4ec0bfb3f166" />


### ORDER BY — Double Sort ASC
> Lowest quantity + month, both ascending

<img width="1277" height="959" alt="image" src="https://github.com/user-attachments/assets/64f0e9b6-3bd9-46bf-9b16-ea2cef72d55c" />


### GROUP BY — Monthly Quantity (customer_order)
> March highest (2,649 units), May lowest (670 units)

<img width="1275" height="959" alt="image" src="https://github.com/user-attachments/assets/b3275078-3c21-48c4-a0e0-a1d90e0cff98" />


### GROUP BY — Monthly Quantity (sales_order)
> February highest (37,722 units), May lowest (33,447 units)

<img width="1279" height="959" alt="image" src="https://github.com/user-attachments/assets/4ca03f95-32bf-42df-9e0b-f90b554f09e1" />

### INNER JOIN — Product + Category
> Joins all 88 products with their category type

<img width="1279" height="958" alt="image" src="https://github.com/user-attachments/assets/de78125d-8940-4d13-a081-778ac12a7a5a" />


### INNER JOIN — High Quantity Filter (>= 595)
> Top 7 selling products with full product details

<img width="1279" height="959" alt="image" src="https://github.com/user-attachments/assets/f53425ea-8fc0-4f10-8068-d03fe88287bc" />


### INNER JOIN — Low Quantity Filter (<= 205)
> 7 lowest selling products with full product details

<img width="1279" height="959" alt="image" src="https://github.com/user-attachments/assets/9aa59221-7d32-4b5e-ac98-8e5a36522b24" />


---

## 🚀 Part 2 — REST API

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/products` | Add a product |
| DELETE | `/products/{id}` | Delete a product |
| GET | `/customers` | List all customers |
| GET | `/customers/{id}` | Get customer by ID |
| POST | `/customers` | Register a customer |
| DELETE | `/customers/{id}` | Delete a customer |
| GET | `/categories` | List all categories |
| POST | `/categories` | Add a category |
| GET | `/orders` | List all orders |
| POST | `/orders` | Place an order |
| GET | `/orders/customer/{id}` | Get orders by customer |
| GET | `/revenue` | Total revenue report |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| SQL Analysis | SQL Server Management Studio |
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## 🏃 How to Run

```bash
# Clone the repo
git clone https://github.com/Nateit1/cafe-sales.git
cd cafe-sales

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your PostgreSQL connection string

# Run the API
uvicorn main:app --reload
```
