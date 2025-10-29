import pika
import time
import json
import os
import sys
import psycopg

# ---------------------------- Configuration ----------------------------

RABBITMQ_CONFIG = {
    "host": "rabbitmq-service",
    "port": 5672,
    "user": "rabbitmq_user",
    "pass": "rabbitmq_password"
}

POSTGRES_CONFIG = {
    "host": "postgres-service",
    "port": 5432,
    "dbname": "mydatabase",
    "user": "admin_user",
    "password": "admin_password"
}

CONSUME_QUEUE = "mul_operations"
RESULT_QUEUE = "mul_result_queue"
DEAD_LETTER_QUEUE = "dead_mul_queue"
ALL_QUEUES = [CONSUME_QUEUE, RESULT_QUEUE, DEAD_LETTER_QUEUE]

TIME_SLEEP = float(os.getenv("TIME_SLEEP", "0"))
MAX_ATTEMPTS = 5
MAX_RETRIES = 15
RETRY_DELAY = 10


# ---------------------------- Database Logic ----------------------------

def get_db_connection():
    conn = psycopg.connect(**POSTGRES_CONFIG)
    conn.autocommit = True
    return conn


def get_number_of_attempts(conn, operation_id: int) -> int | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT number_of_attempts FROM public.operations WHERE operation_id = %s",
            (operation_id,)
        )
        result = cur.fetchone()
        return result[0] if result else None


def update_number_of_attempts(conn, operation_id: int, new_attempts: int):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE public.operations SET number_of_attempts = %s WHERE operation_id = %s",
            (new_attempts, operation_id)
        )


# ---------------------------- RabbitMQ Logic ----------------------------

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_CONFIG["user"], RABBITMQ_CONFIG["pass"])
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_CONFIG["host"],
        port=RABBITMQ_CONFIG["port"],
        credentials=credentials
    )
    for attempt in range(MAX_RETRIES):
        try:
            connection = pika.BlockingConnection(parameters)
            print("[INFO] Connected to RabbitMQ", flush=True)
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[WARN] RabbitMQ connection failed: {e}. Retrying in {RETRY_DELAY}s...", flush=True)
            time.sleep(RETRY_DELAY)
    raise Exception("Failed to connect to RabbitMQ after retries.")


def declare_queues(channel):
    for q in ALL_QUEUES:
        channel.queue_declare(queue=q, durable=True)


def send_to_queue(channel, queue_name, data):
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[INFO] Sent to {queue_name}: {data}", flush=True)


# ---------------------------- Processing Logic ----------------------------

def simulate_processing(seconds):
    for i in range(int(seconds)):
        print(f"[DEBUG] Processing step {i+1}/{int(seconds)}", flush=True)
        time.sleep(1)


def handle_operation(channel, conn, data):
    try:
        num1 = data["num1"]
        num2 = data["num2"]
        clientId = data["clientId"]
        operation_id = data["operation_id"]
    except KeyError as e:
        print(f"[ERROR] Missing key in message: {e}", flush=True)
        return

    attempts = get_number_of_attempts(conn, operation_id)
    if attempts is None:
        print(f"[WARN] operation_id {operation_id} not found", flush=True)
        return

    if attempts >= MAX_ATTEMPTS:
        print(f"[INFO] Max attempts reached for operation_id={operation_id}. Sending to {DEAD_LETTER_QUEUE}.", flush=True)
        send_to_queue(channel, DEAD_LETTER_QUEUE, data)
        return

    update_number_of_attempts(conn, operation_id, attempts + 1)
    simulate_processing(TIME_SLEEP)

    result = num1 * num2
    result_data = {
        "num1": num1,
        "num2": num2,
        "result": result,
        "operation": "multiply",
        "clientId": clientId,
        "operation_id": operation_id
    }

    send_to_queue(channel, RESULT_QUEUE, result_data)
    print(f"[INFO] Operation successful: {num1} * {num2} = {result}", flush=True)


# ---------------------------- Callback & Start ----------------------------

def on_message(channel, conn):
    def callback(ch, method, properties, body):
        try:
            message_str = body.decode("utf-8")
            data = json.loads(message_str)
            print(f"[INFO] Received from {method.routing_key}: {data}", flush=True)
            handle_operation(channel, conn, data)
        except json.JSONDecodeError:
            print("[ERROR] Failed to decode JSON", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    return callback


def main():
    print("[BOOT] Starting mul_operations service...", flush=True)

    conn = get_db_connection()
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    declare_queues(channel)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=CONSUME_QUEUE, on_message_callback=on_message(channel, conn))

    print(f"[INFO] Waiting for messages on '{CONSUME_QUEUE}'. Press CTRL+C to exit.", flush=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("[INFO] Gracefully shutting down...", flush=True)
        channel.stop_consuming()


if __name__ == "__main__":
    main()
