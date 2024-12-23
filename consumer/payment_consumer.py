import boto3
import json
from cassandra.cluster import Cluster

# Initialize SQS client
sqs = boto3.client('sqs', region_name='your-region')
queue_url = 'https://sqs.your-region.amazonaws.com/your-account-id/payments_data'

# Connect to local Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('ecom_store')

def process_payment_message(message_body):
    payment = json.loads(message_body)
    session.execute("""
        UPDATE orders_payments_facts
        SET payment_id = %s, payment_method = %s, payment_status = %s, payment_datetime = %s
        WHERE order_id = %s
    """, (payment['payment_id'], payment['payment_method'], payment['payment_status'], payment['payment_datetime'], payment['order_id']))
    print(f"Payment processed and updated in Cassandra: {payment}")

def poll_messages():
    while True:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)
        if 'Messages' in response:
            for message in response['Messages']:
                process_payment_message(message['Body'])
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

if __name__ == "__main__":
    poll_messages()
