USE globaltech_ecommerce;

-- 1. Basic Counts
SELECT COUNT(*) as total_customers FROM Customers;
SELECT COUNT(*) as total_orders FROM Orders;
SELECT COUNT(*) as total_products FROM Products;

-- 2. Distribution of Customers by Segment
SELECT segment, COUNT(customer_id) as customer_count,
       ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM Customers), 2) as percentage
FROM Customers
GROUP BY segment
ORDER BY customer_count DESC;

-- 3. Distribution of Products by Category
SELECT category, COUNT(product_id) as product_count
FROM Products
GROUP BY category
ORDER BY product_count DESC;

-- 4. Order Volume over Time (Year-Month)
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as order_month,
    COUNT(order_id) as num_orders
FROM Orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;

-- 5. Summary Statistics of Order Items
SELECT 
    MIN(quantity) as min_qty,
    MAX(quantity) as max_qty,
    AVG(quantity) as avg_qty,
    MIN(discount) as min_discount,
    MAX(discount) as max_discount
FROM Order_Items;
