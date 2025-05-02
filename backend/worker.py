import pika
import psycopg2
import time
import os

DB_HOST = os.getenv("DB_HOST", "db")  # fallback default
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
    # Decode the message
    message = body.decode()
    print(f"🍩 Received order message: {message}")

    # Extract order_id from the message (assuming the message format is "Order ID: <id>, Product ID: <id>")
    try:
        # Example message format: "Order ID: 2, Product ID: 1"
        order_id = int(message.split(",")[0].split(":")[1].strip())
        product_id = int(message.split(",")[1].split(":")[1].strip())
        print(f"✅ Successfully extracted Order ID: {order_id}, Product ID: {product_id}")
    except Exception as e:
        print(f"❌ Failed to parse order details: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message even if it fails
        return

    # Add a 10-second delay before updating the order status
    print("⏳ Waiting for 10 seconds before updating the order status...")
    time.sleep(10)  # Delay for 10 seconds

    # Update the order status in the database
    try:
        print(f"🔄 Updating order {order_id} status to 'completed'...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Update the status of the order to 'completed'
        cur.execute("UPDATE orders SET status = %s WHERE id = %s;", ('completed', order_id))
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

        print(f"✅ Order {order_id} marked as completed.")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message after processing
    except Exception as e:
        print(f"❌ Failed to update order status for order {order_id}: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message even in case of failure

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

    # Start consuming messages from the queue
    channel.basic_consume(
        queue='orders_queue',
        on_message_callback=callback,
        auto_ack=False  # Disable auto-acknowledge; we will manually acknowledge
    )

    print("🍪 Worker is running, press CTRL+C to exit.")
    channel.start_consuming()
except Exception as e:
    print(f"❌ Error setting up RabbitMQ channel: {e}")
