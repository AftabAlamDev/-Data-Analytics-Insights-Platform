import nbformat as nbf

nb = nbf.v4.new_notebook()

text_intro = """\
# GlobalTech E-Commerce: Exploratory Data Analysis & Statistics
This notebook performs deep-dive analysis on the generated dataset.
We will cover:
1. Data Loading and Cleaning
2. Exploratory Data Analysis (EDA)
3. Statistical Analysis (Hypothesis Testing & Correlation)
4. Feature Engineering
5. Business Conclusions
"""

code_imports = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set plot style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
"""

text_load = """\
## 1. Data Loading & Joining
We will load the raw CSV files generated previously and join them for comprehensive analysis.
"""

code_load = """\
customers = pd.read_csv('../data/raw/customers.csv')
products = pd.read_csv('../data/raw/products.csv')
orders = pd.read_csv('../data/raw/orders.csv')
order_items = pd.read_csv('../data/raw/order_items.csv')

# Join data
df = orders.merge(customers, on='customer_id')
df = df.merge(order_items, on='order_id')
df = df.merge(products, on='product_id')

# Convert dates
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# Basic understanding
print(f"Total Records: {len(df)}")
df.head()
"""

text_clean = """\
## 2. Data Cleaning & Feature Engineering
Let's check for missing values, duplicates, and create new features.
"""

code_clean = """\
# Missing values
print("Missing Values:\\n", df.isnull().sum())

# Duplicates
print("\\nDuplicate Rows:", df.duplicated().sum())

# Feature Engineering: Profit Margin and Delivery Time
df['profit'] = df['total_price'] - (df['unit_cost'] * df['quantity'])
df['profit_margin'] = df['profit'] / df['total_price']
df['delivery_days'] = (df['ship_date'] - df['order_date']).dt.days

# Handle any anomalies
df = df[df['quantity'] > 0] # Ensure valid quantities
df.head()
"""

text_eda = """\
## 3. Exploratory Data Analysis (EDA)
Let's explore sales trends, regional performance, and customer segmentation.
"""

code_eda = """\
# 3.1 Sales by Category
category_sales = df.groupby('category')['total_price'].sum().reset_index()
sns.barplot(x='category', y='total_price', data=category_sales)
plt.title('Total Revenue by Product Category')
plt.ylabel('Revenue ($)')
plt.show()

# 3.2 Sales over Time
df_monthly = df.set_index('order_date').resample('ME')['total_price'].sum()
df_monthly.plot(title='Monthly Revenue Trend')
plt.ylabel('Revenue ($)')
plt.show()
"""

text_stats = """\
## 4. Statistical Analysis
We will perform statistical tests to uncover deeper insights.

### 4.1 Correlation Analysis
Is there a relationship between discount offered and quantity ordered?
"""

code_stats1 = """\
correlation = df['discount'].corr(df['quantity'])
print(f"Correlation between Discount and Quantity: {correlation:.3f}")

# Visualizing correlation matrix for numerical features
num_cols = ['quantity', 'unit_price_x', 'discount', 'total_price', 'profit', 'delivery_days']
sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()
"""

text_stats2 = """\
### 4.2 Hypothesis Testing (Two-Sample T-Test)
**Business Question:** Do 'Consumer' segment customers generate significantly higher average profit per order item than 'Corporate' customers?

- $H_0$: There is no difference in mean profit between Consumer and Corporate segments.
- $H_a$: There is a significant difference.
"""

code_stats2 = """\
consumer_profit = df[df['segment'] == 'Consumer']['profit']
corporate_profit = df[df['segment'] == 'Corporate']['profit']

t_stat, p_val = stats.ttest_ind(consumer_profit, corporate_profit, equal_var=False)
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4f}")

alpha = 0.05
if p_val < alpha:
    print("Conclusion: Reject Null Hypothesis. There is a statistically significant difference.")
else:
    print("Conclusion: Fail to Reject Null Hypothesis. No significant difference found.")
"""

text_excel = """\
## 5. Exporting Summary for Excel
We will create a pivot table of Region vs Category Sales and export it to an Excel file.
"""

code_excel = """\
# Create Pivot Table
pivot = pd.pivot_table(df, values='total_price', index='region', columns='category', aggfunc='sum', fill_value=0)

# Export to Excel
pivot.to_excel('../excel/analysis.xlsx', sheet_name='Regional_Sales')
print("Successfully exported Excel analysis to ../excel/analysis.xlsx")

# Also save the cleaned joined dataframe for Power BI (optional, but good practice)
df.to_csv('../data/cleaned/consolidated_sales.csv', index=False)
print("Saved consolidated data for Power BI.")
"""

text_conclusions = """\
## 6. Business Conclusions & Key Findings
1. **Trend Analysis:** The monthly revenue trend shows specific seasonality (depending on the generated seed).
2. **Correlation:** The correlation matrix shows how discounts impact overall profitability but might not strongly drive higher quantities, suggesting a review of the discount strategy.
3. **Statistical Insight:** The T-test confirms whether our distinct customer segments inherently behave differently in terms of profitability. This directly impacts targeted marketing spend.
"""


nb['cells'] = [
    nbf.v4.new_markdown_cell(text_intro),
    nbf.v4.new_code_cell(code_imports),
    nbf.v4.new_markdown_cell(text_load),
    nbf.v4.new_code_cell(code_load),
    nbf.v4.new_markdown_cell(text_clean),
    nbf.v4.new_code_cell(code_clean),
    nbf.v4.new_markdown_cell(text_eda),
    nbf.v4.new_code_cell(code_eda),
    nbf.v4.new_markdown_cell(text_stats),
    nbf.v4.new_code_cell(code_stats1),
    nbf.v4.new_markdown_cell(text_stats2),
    nbf.v4.new_code_cell(code_stats2),
    nbf.v4.new_markdown_cell(text_excel),
    nbf.v4.new_code_cell(code_excel),
    nbf.v4.new_markdown_cell(text_conclusions)
]

with open('data_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)
    
print("Jupyter Notebook created successfully.")
