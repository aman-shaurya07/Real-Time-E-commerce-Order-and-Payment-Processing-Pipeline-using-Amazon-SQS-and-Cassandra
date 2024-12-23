import boto3
import json
import random
import time

# Initialize SQS client
sqs = boto3.client('sqs', region_name='your-region')

# Queue URL
orders_queue_url = 'https://sqs.your-region.amazonaws.com/your-account-id/orders_data'

def send_order_message(order):
    response = sqs.send_message(
        QueueUrl=orders_queue_url,
        MessageBody=json.dumps(order)
    )
    print(f"Order message sent: {response['MessageId']}")

def generate_mock_order(order_id):
    items = ["Laptop", "Phone", "Tablet", "Monitor"]
    return {
        "order_id": order_id,
        "customer_id": random.randint(100, 1000),
        "item": random.choice(items),
        "quantity": random.randint(1, 10),
        "price": random.uniform(100, 1000),
        "creation_date": "2024-01-21"
    }

if __name__ == "__main__":
    for order_id in range(1, 101):
        order = generate_mock_order(order_id)
        send_order_message(order)
        time.sleep(2)
