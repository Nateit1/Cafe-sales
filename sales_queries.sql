-- ============================================================
-- CafeSales — SQL Query Collection
-- Database: Cafe_Sales
-- Tables: Customer, Customer_Order, Product, Product_Category, Sales_Order
-- ============================================================


-- ── STEP 1: ORDER BY ─────────────────────────────────────────────────────────

-- Q1a: Single sort — highest quantity (DESC)
SELECT * FROM customer_order ORDER BY quantity DESC;
-- Result: C266 purchased Product 509 in Mar with quantity 79 (most)

-- Q1b: Double sort — highest quantity, then by month (DESC)
SELECT * FROM customer_order ORDER BY quantity DESC, month DESC;

-- Q1c: Single sort — lowest quantity (ASC)
SELECT * FROM customer_order ORDER BY quantity;
-- Result: C196 purchased Product 109 in Feb with quantity 10 (least)

-- Q1d: Double sort — lowest quantity, then by month (ASC)
SELECT * FROM customer_order ORDER BY Quantity ASC, month ASC;


-- ── STEP 2: GROUP BY ─────────────────────────────────────────────────────────

-- Q2: Total quantity sold per month from customer_order (DESC)
SELECT sum(quantity), month
FROM customer_order
GROUP BY month
ORDER BY sum(quantity) DESC;
-- Result: Mar = 2649, Feb = 2185, Jan = 2112, Apr = 1738, May = 670

-- Q3: Total sold quantity per month from sales_order (DESC)
SELECT sum(Sold_quantity), month
FROM sales_order
GROUP BY month
ORDER BY sum(sold_quantity) DESC;
-- Result: Feb = 37722 (highest), May = 33447 (lowest)


-- ── STEP 3: JOINS ─────────────────────────────────────────────────────────────

-- Q4: INNER JOIN — Products with their category
SELECT * FROM product
INNER JOIN product_category
ON product.category_ID = Product_category.category_ID;
-- Returns 88 rows — all products joined with category type

-- Q5: INNER JOIN — Sales orders with products (high quantity filter)
SELECT * FROM sales_order
INNER JOIN product
ON product.product_ID = sales_order.product_ID
WHERE sales_order.sold_quantity >= 595;
-- Returns 7 rows — top selling products (French Vanilla, Chocolate Amaretto, etc.)

-- Q6: INNER JOIN — Sales orders with products (low quantity filter)
SELECT * FROM sales_order
INNER JOIN product
ON product.product_ID = sales_order.product_ID
WHERE sales_order.sold_quantity <= 205;
-- Returns 7 rows — lowest selling products (Apple Spice, Buche de Noel, etc.)
