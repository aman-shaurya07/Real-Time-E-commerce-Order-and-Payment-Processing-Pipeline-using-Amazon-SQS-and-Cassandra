import boto3
import json
from cassandra.cluster import Cluster

# Initialize SQS client
sqs = boto3.client('sqs', region_name='your-region')
queue_url = 'https://sqs.your-region.amazonaws.com/your-account-id/orders_data'

# Connect to local Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('ecom_store')

def process_order_message(message_body):
    order = json.loads(message_body)
    session.execute("""
        INSERT INTO orders_payments_facts (order_id, customer_id, item, quantity, price, shipping_address, order_status, creation_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (order['order_id'], order['customer_id'], order['item'], order['quantity'], order['price'], "Default Address", "Pending", order['creation_date']))
    print(f"Order processed and inserted into Cassandra: {order}")

def poll_messages():
    while True:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)
        if 'Messages' in response:
            for message in response['Messages']:
                process_order_message(message['Body'])
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

if __name__ == "__main__":
    poll_messages()
