CREATE KEYSPACE IF NOT EXISTS ecom_store WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE ecom_store;

CREATE TABLE orders_payments_facts (
    order_id INT PRIMARY KEY,
    customer_id INT,
    item TEXT,
    quantity INT,
    price FLOAT,
    shipping_address TEXT,
    order_status TEXT,
    creation_date TEXT,
    payment_id INT,
    payment_method TEXT,
    payment_status TEXT,
    payment_datetime TEXT
);
