import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:Aftab%40786@localhost/globaltech_ecommerce')

print("Loading Customers...")
customers = pd.read_csv('../data/raw/customers.csv')
customers.to_sql('Customers', con=engine, if_exists='append', index=False)

print("Loading Products...")
products = pd.read_csv('../data/raw/products.csv')
products.to_sql('Products', con=engine, if_exists='append', index=False)

print("Loading Orders...")
orders = pd.read_csv('../data/raw/orders.csv')
orders.to_sql('Orders', con=engine, if_exists='append', index=False)

print("Loading Order_Items...")
order_items = pd.read_csv('../data/raw/order_items.csv')
order_items.to_sql('Order_Items', con=engine, if_exists='append', index=False)

print("Data loaded successfully!")
