USE globaltech_ecommerce;

-- 1. Total Revenue, Cost, and Profit
SELECT 
    SUM(total_price) as total_revenue,
    SUM(total_cost) as total_cost,
    SUM(profit) as total_profit,
    (SUM(profit) / SUM(total_price)) * 100 as profit_margin_pct
FROM vw_sales_data;

-- 2. Regional Performance
SELECT 
    region,
    COUNT(DISTINCT order_id) as num_orders,
    SUM(total_price) as revenue,
    SUM(profit) as profit
FROM vw_sales_data
GROUP BY region
ORDER BY revenue DESC;

-- 3. Top 10 Best-Selling Products by Revenue
SELECT 
    product_id,
    category,
    sub_category,
    SUM(quantity) as total_units_sold,
    SUM(total_price) as total_revenue
FROM vw_sales_data
GROUP BY product_id, category, sub_category
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. Category Performance Breakdown
SELECT 
    category,
    SUM(total_price) as revenue,
    SUM(profit) as profit,
    (SUM(profit) / SUM(total_price)) * 100 as profit_margin
FROM vw_sales_data
GROUP BY category
ORDER BY profit DESC;

-- 5. Customer Value (Average Order Value)
SELECT 
    COUNT(DISTINCT order_id) as total_orders,
    SUM(total_price) as total_revenue,
    SUM(total_price) / COUNT(DISTINCT order_id) as average_order_value
FROM vw_sales_data;
