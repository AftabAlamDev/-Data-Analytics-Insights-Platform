USE globaltech_ecommerce;

-- 1. Identify Missing Values in Customers
SELECT COUNT(*) as missing_emails FROM Customers WHERE email IS NULL OR email = '';

-- 2. Standardize Text Formats
UPDATE Customers 
SET city = UPPER(city), 
    country = UPPER(country);

-- 3. Check for Duplicate Orders (Sanity Check)
SELECT order_id, COUNT(*) 
FROM Orders 
GROUP BY order_id 
HAVING COUNT(*) > 1;

-- 4. Create a View for Cleaned and Consolidated Sales Data
-- This view will be useful for subsequent analytical queries and for Power BI
CREATE OR REPLACE VIEW vw_sales_data AS
SELECT 
    o.order_id,
    o.order_date,
    o.ship_date,
    o.ship_mode,
    o.region,
    c.customer_id,
    c.segment,
    c.country,
    c.city,
    oi.product_id,
    p.category,
    p.sub_category,
    oi.quantity,
    oi.unit_price,
    oi.discount,
    oi.total_price,
    (p.unit_cost * oi.quantity) as total_cost,
    (oi.total_price - (p.unit_cost * oi.quantity)) as profit
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id;

-- 5. Detect Outliers in Quantity (e.g., incredibly high quantities)
SELECT * FROM Order_Items WHERE quantity > 100;
