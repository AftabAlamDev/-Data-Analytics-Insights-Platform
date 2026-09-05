# Power BI Dashboard Implementation Guide

Since binary `.pbix` files cannot be generated directly via code, this guide provides the exact specifications to build the requested "GlobalTech E-Commerce Insights" dashboard.

## 1. Data Model (Star Schema)

Import the 4 cleaned tables (or directly connect to the MySQL Database). Set up the relationships as follows:

- **Fact Table:** `Orders` & `Order_Items` (Merge these in Power Query to create a `Sales_Fact` table).
- **Dimension Tables:** `Customers`, `Products`, and a newly created `Date_Dim` table.

**Relationships:**
- `Customers[customer_id]` (1) -> (*) `Sales_Fact[customer_id]`
- `Products[product_id]` (1) -> (*) `Sales_Fact[product_id]`
- `Date_Dim[Date]` (1) -> (*) `Sales_Fact[order_date]`

## 2. Key DAX Measures

Create a new table for Measures and add the following:

```dax
Total Revenue = SUM(Sales_Fact[total_price])

Total Cost = SUMX(Sales_Fact, Sales_Fact[unit_cost] * Sales_Fact[quantity])

Total Profit = [Total Revenue] - [Total Cost]

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(Sales_Fact[order_id])

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

YoY Revenue Growth = 
VAR CurrentRevenue = [Total Revenue]
VAR PrevYearRevenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Date_Dim[Date]))
RETURN DIVIDE(CurrentRevenue - PrevYearRevenue, PrevYearRevenue, 0)
```

## 3. Dashboard Pages Layout

### Page 1: Executive Overview
**Goal:** High-level performance KPIs.
- **Visuals:** 
  - KPI Cards for Total Revenue, Total Profit, Profit Margin, and Total Orders.
  - Line Chart: Revenue & Profit by Month/Year (using `Date_Dim`).
  - Donut Chart: Revenue by Customer Segment.
  - Map Visual: Revenue by Country/Region.

### Page 2: Sales/Performance Analysis
**Goal:** Deep dive into product and category performance.
- **Visuals:**
  - Matrix Table: Category and Sub-category broken down by Revenue, Units Sold, and Profit Margin.
  - Bar Chart: Top 10 Products by Revenue.
  - Waterfall Chart: Profit breakdown by Category.

### Page 3: Customer Analysis
**Goal:** Understand customer behavior.
- **Visuals:**
  - Scatter Plot: Customer Profitability (X-axis: Total Orders, Y-axis: Profit Margin %, Size: Revenue).
  - Bar Chart: Revenue by Segment (Consumer vs. Corporate vs. Home Office).
  - Table: RFM Score details (from SQL advanced analysis) imported as a separate table.

### Page 4: Insights / Recommendations
**Goal:** Textual analysis and actionable insights.
- **Visuals:** Use Smart Narratives and Text Boxes.
- **Example Insights to display:**
  - *"Corporate segment yields a statistically significant higher profit margin despite lower total transaction volume."*
  - *"Discounting strategies on 'Furniture' are negatively impacting net margins; recommend reducing discounts by 5% in Q4."*
```
