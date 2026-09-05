import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Ensure directories exist
os.makedirs('../data/raw', exist_ok=True)
os.makedirs('../data/cleaned', exist_ok=True)

# 1. Generate Customers
num_customers = 5000
customer_ids = [f"CUST-{str(i).zfill(5)}" for i in range(1, num_customers + 1)]
segments = ['Consumer', 'Corporate', 'Home Office']
countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'Australia']
cities = ['New York', 'Los Angeles', 'London', 'Berlin', 'Sydney', 'Toronto', 'Chicago', 'Manchester', 'Munich', 'Melbourne']

customers_data = {
    'customer_id': customer_ids,
    'first_name': [f"FirstName_{i}" for i in range(num_customers)],
    'last_name': [f"LastName_{i}" for i in range(num_customers)],
    'email': [f"user{i}@example.com" for i in range(num_customers)],
    'country': np.random.choice(countries, num_customers, p=[0.4, 0.2, 0.15, 0.15, 0.1]),
    'city': np.random.choice(cities, num_customers),
    'segment': np.random.choice(segments, num_customers, p=[0.6, 0.25, 0.15]),
    'registration_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000)) for _ in range(num_customers)]
}
df_customers = pd.DataFrame(customers_data)
df_customers.to_csv('../data/raw/customers.csv', index=False)
print("Generated customers.csv")

# 2. Generate Products
categories = ['Electronics', 'Furniture', 'Office Supplies']
sub_categories = {
    'Electronics': ['Laptops', 'Smartphones', 'Tablets', 'Accessories'],
    'Furniture': ['Chairs', 'Tables', 'Desks', 'Bookcases'],
    'Office Supplies': ['Paper', 'Pens', 'Binders', 'Storage']
}

products_data = []
product_id_counter = 1
for cat in categories:
    for sub_cat in sub_categories[cat]:
        # Generate 10-30 products per sub_category
        num_prods = random.randint(10, 30)
        for _ in range(num_prods):
            unit_cost = round(random.uniform(10, 800), 2)
            unit_price = round(unit_cost * random.uniform(1.2, 2.0), 2)
            products_data.append({
                'product_id': f"PROD-{str(product_id_counter).zfill(4)}",
                'product_name': f"{sub_cat} Model {random.randint(100,999)}",
                'category': cat,
                'sub_category': sub_cat,
                'unit_cost': unit_cost,
                'unit_price': unit_price
            })
            product_id_counter += 1

df_products = pd.DataFrame(products_data)
df_products.to_csv('../data/raw/products.csv', index=False)
print("Generated products.csv")

# 3. Generate Orders
num_orders = 25000
order_ids = [f"ORD-{str(i).zfill(6)}" for i in range(1, num_orders + 1)]
regions = ['North', 'South', 'East', 'West', 'Central']
ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

orders_data = {
    'order_id': order_ids,
    'customer_id': np.random.choice(customer_ids, num_orders),
    'order_date': [datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1000)) for _ in range(num_orders)],
    'ship_mode': np.random.choice(ship_modes, num_orders, p=[0.6, 0.2, 0.15, 0.05]),
    'region': np.random.choice(regions, num_orders)
}
df_orders = pd.DataFrame(orders_data)
# Ensure ship date is after order date
df_orders['ship_date'] = df_orders['order_date'] + pd.to_timedelta(np.random.randint(1, 7, num_orders), unit='d')
df_orders.to_csv('../data/raw/orders.csv', index=False)
print("Generated orders.csv")

# 4. Generate Order Items
product_ids = df_products['product_id'].tolist()
product_prices = dict(zip(df_products['product_id'], df_products['unit_price']))

order_items_data = []
item_id_counter = 1

for order_id in order_ids:
    num_items = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.08, 0.02])
    # Pick random products for this order
    chosen_products = np.random.choice(product_ids, num_items, replace=False)
    for prod_id in chosen_products:
        qty = random.randint(1, 10)
        # Apply discount randomly (0%, 5%, 10%, 15%, 20%)
        discount = np.random.choice([0.0, 0.05, 0.1, 0.15, 0.2], p=[0.7, 0.1, 0.1, 0.05, 0.05])
        unit_price = product_prices[prod_id]
        total_price = round(qty * unit_price * (1 - discount), 2)
        
        order_items_data.append({
            'order_item_id': f"ITEM-{str(item_id_counter).zfill(7)}",
            'order_id': order_id,
            'product_id': prod_id,
            'quantity': qty,
            'unit_price': unit_price,
            'discount': discount,
            'total_price': total_price
        })
        item_id_counter += 1

df_order_items = pd.DataFrame(order_items_data)
df_order_items.to_csv('../data/raw/order_items.csv', index=False)
print("Generated order_items.csv")

print("Data generation complete!")
