import pika
import psycopg2
import time
import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

# Connect to the PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port="5432"
    )

# Define the callback function for processing messages
def callback(ch, method, properties, body):
    message = body.decode()
    print(f"🍩 Received order message: {message}")

    try:
        order_id = int(message.split(",")[0].split(":")[1].strip())
        product_id = int(message.split(",")[1].split(":")[1].strip())
        print(f"✅ Successfully extracted Order ID: {order_id}, Product ID: {product_id}")
    except Exception as e:
        print(f"❌ Failed to parse order details: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # No longer updating order status
    print("📨 Order processed without updating status.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Retry RabbitMQ connection until it's ready
print("🔄 Attempting to connect to RabbitMQ...")
for i in range(10):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            )
        )
        print("✅ Connected to RabbitMQ!")
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"🔁 Attempt {i+1}/10: RabbitMQ not ready, retrying in 3 seconds...")
        time.sleep(3)
else:
    print("❌ Could not connect to RabbitMQ after multiple attempts.")
    exit(1)

# Setup RabbitMQ channel and start consuming
try:
    channel = connection.channel()
    channel.queue_declare(queue='orders_queue')
    print("📦 Waiting for orders...")

    channel.basic_consume(
        queue='orders_queue',
        on_message_callback=callback,
        auto_ack=False
    )

    print("🍪 Worker is running, press CTRL+C to exit.")
    channel.start_consuming()
except Exception as e:
    print(f"❌ Error setting up RabbitMQ channel: {e}")
