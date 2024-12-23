import boto3
import json
import random
import time

# Initialize SQS client
sqs = boto3.client('sqs', region_name='your-region')

# Queue URL
payments_queue_url = 'https://sqs.your-region.amazonaws.com/your-account-id/payments_data'

def send_payment_message(payment):
    response = sqs.send_message(
        QueueUrl=payments_queue_url,
        MessageBody=json.dumps(payment)
    )
    print(f"Payment message sent: {response['MessageId']}")

def generate_mock_payment(order_id):
    payment_methods = ["Credit Card", "Debit Card", "PayPal", "Google Pay"]
    return {
        "payment_id": order_id + 1000,
        "order_id": order_id,
        "payment_method": random.choice(payment_methods),
        "payment_status": "Completed",
        "payment_datetime": "2024-01-21T10:00:00Z"
    }

if __name__ == "__main__":
    for order_id in range(1, 101):
        payment = generate_mock_payment(order_id)
        send_payment_message(payment)
        time.sleep(2)
