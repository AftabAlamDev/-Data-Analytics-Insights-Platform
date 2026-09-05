USE globaltech_ecommerce;

-- 1. Running Total of Revenue per Month (Using Window Functions)
WITH MonthlyRevenue AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') as order_month,
        SUM(total_price) as monthly_revenue
    FROM vw_sales_data
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    order_month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (ORDER BY order_month) as running_total_revenue
FROM MonthlyRevenue;

-- 2. Year-over-Year (YoY) Growth Percentage
WITH YearlySales AS (
    SELECT 
        YEAR(order_date) as sales_year,
        SUM(total_price) as total_revenue
    FROM vw_sales_data
    GROUP BY YEAR(order_date)
)
SELECT 
    sales_year,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY sales_year) as previous_year_revenue,
    ((total_revenue - LAG(total_revenue) OVER (ORDER BY sales_year)) / LAG(total_revenue) OVER (ORDER BY sales_year)) * 100 as yoy_growth_pct
FROM YearlySales;

-- 3. Customer RFM Segmentation (Recency, Frequency, Monetary)
-- Base CTE
WITH CustomerRFM AS (
    SELECT 
        customer_id,
        MAX(order_date) as last_order_date,
        DATEDIFF((SELECT MAX(order_date) FROM vw_sales_data), MAX(order_date)) as recency_days, 
        COUNT(DISTINCT order_id) as frequency,
        SUM(total_price) as monetary_value
    FROM vw_sales_data
    GROUP BY customer_id
)
SELECT 
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    NTILE(4) OVER (ORDER BY recency_days ASC) as R_Score, -- 4 is best (most recent)
    NTILE(4) OVER (ORDER BY frequency DESC) as F_Score, -- 4 is best (highest freq)
    NTILE(4) OVER (ORDER BY monetary_value DESC) as M_Score -- 4 is best (highest spend)
FROM CustomerRFM;

-- 4. Customer Retention (Repeat vs One-time buyers)
WITH CustomerOrders AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) as order_count
    FROM Orders
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN order_count = 1 THEN 'One-time Buyer'
        ELSE 'Repeat Customer'
    END as customer_type,
    COUNT(customer_id) as num_customers,
    (COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM Customers)) as pct_of_total
FROM CustomerOrders
GROUP BY customer_type;

-- 5. Moving Average (3-month moving average of revenue)
WITH MonthlyRevenue AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m-01') as month_start,
        SUM(total_price) as revenue
    FROM vw_sales_data
    GROUP BY DATE_FORMAT(order_date, '%Y-%m-01')
)
SELECT 
    month_start,
    revenue,
    AVG(revenue) OVER (
        ORDER BY month_start 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3m
FROM MonthlyRevenue;
