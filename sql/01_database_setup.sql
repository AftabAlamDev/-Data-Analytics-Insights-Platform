-- Create Database
CREATE DATABASE IF NOT EXISTS globaltech_ecommerce;
USE globaltech_ecommerce;

-- Create Customers Table
CREATE TABLE Customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    country VARCHAR(100),
    city VARCHAR(100),
    segment VARCHAR(50),
    registration_date DATE
);

-- Create Products Table
CREATE TABLE Products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    unit_cost DECIMAL(10, 2),
    unit_price DECIMAL(10, 2)
);

-- Create Orders Table
CREATE TABLE Orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    region VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Create Order Items Table
CREATE TABLE Order_Items (
    order_item_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(10, 2),
    discount DECIMAL(4, 2),
    total_price DECIMAL(12, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Note: Use standard local infile commands or import wizards to load the generated CSV files into these tables.
