# Real-Time E-commerce Order and Payment Processing Pipeline using Amazon SQS and Cassandra

## Overview

This project simulates a real-time data processing pipeline for an e-commerce platform, showcasing the integration of **Amazon SQS** for messaging and a **local Cassandra database** for storage. The pipeline processes mock `orders` and `payments` data, ensuring a decoupled and scalable architecture. 

Key highlights:
1. **Data Producers** generate mock data for `orders` and `payments`, publishing the messages to respective SQS queues.
2. **Data Consumers** retrieve the messages from the SQS queues and store them in a local Cassandra database.
3. A unified **Cassandra table** stores processed data in a denormalized format, ready for analytics or reporting.

This project demonstrates the use of distributed systems for real-time data ingestion, processing, and storage while maintaining the simplicity of local development for the database layer.

---

## Project Workflow

1. **Data Generation (Producers)**:
   - The `order_producer.py` generates mock order data (e.g., `order_id`, `customer_id`, `item`, `quantity`, `price`, etc.) and publishes it to the **SQS queue `orders_data`**.
   - The `payment_producer.py` generates mock payment data (e.g., `payment_id`, `order_id`, `payment_method`, `payment_status`, etc.) and publishes it to the **SQS queue `payments_data`**.

2. **Data Consumption (Consumers)**:
   - **Order Consumer**:
     - Reads messages from the `orders_data` queue.
     - Inserts the `order` data into a Cassandra table.
   - **Payment Consumer**:
     - Reads messages from the `payments_data` queue.
     - Updates the corresponding order entry in Cassandra with payment details.

3. **Database Layer**:
   - A **denormalized Cassandra table** (`orders_payments_facts`) stores both order and payment details for quick and efficient querying.
   - The table schema allows integration of order and payment data into a single, analytics-ready format.

4. **Real-World Applications**:
   - Such pipelines are widely used in e-commerce platforms, where order and payment data need to be processed and stored in real time for further analysis, fraud detection, or reporting.

---

## Architecture Diagram

```plaintext
  +---------------+       +------------------+
  | Order Producer|       | Payment Producer |
  +-------+-------+       +-------+----------+
          |                       |
          | Publish Orders         | Publish Payments
          v                       v
  +-------+-------+       +-------+----------+
  |   SQS Orders  |       |   SQS Payments   |
  +---------------+       +------------------+
          |                       |
          | Consume Orders         | Consume Payments
          v                       v
  +---------------+       +------------------+
  | Order Consumer|       | Payment Consumer |
  +-------+-------+       +-------+----------+
          |                       |
          | Insert into Cassandra | Update Order in Cassandra
          v                       v
  +-------------------------------------------+
  |     Local Cassandra (orders_payments_facts)|
  +-------------------------------------------+



## Instructions

Step 1. **Setup Cassandra**:
Install Docker and run Cassandra using the provided Docker Compose file:
```bash
cd cassandra
docker-compose up -d
```

Set up the database schema by executing the schema.cql file in cqlsh:
```bash
docker exec -it cassandra-db cqlsh
SOURCE 'schema.cql';
```

Step 2. **Set Up AWS SQS**
1. Log in to your AWS Management Console.
2. Create two SQS queues:
    - orders_data
    - payments_data
3. Note down the Queue URLs for use in the producer and consumer scripts.

Step 3: **Install Dependencies**
```bash
cd producer
pip install -r requirements.txt
```

Step 4. **Run Producers:**
```bash
python3 producer/order_producer.py
python3 producer/payment_producer.py
```

Step 5. **Run Consumers:**
```bash
python3 consumer/order_consumer.py
python3 consumer/payment_consumer.py
```

Step 6. **Verify Data**
Query the Cassandra database to verify that orders and payments are correctly processed and stored:
```bash
SELECT * FROM ecom_store.orders_payments_facts;
```