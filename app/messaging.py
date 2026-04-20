import pika
import json
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "execution_events"

def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    return connection

# ── Publisher — sends event to queue ──────────────────────────
def publish_event(event: dict):
    try:
        connection = get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        print(f"Event published to queue: {event['event_type']}")
    except Exception as e:
        print(f"RabbitMQ publish error: {e}")

# ── Consumer — reads events from queue ────────────────────────
def start_consumer(db_session_factory):
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body)
            print(f"Received event: {event['event_type']}")

            from app.models.models import AuditEvent
            import uuid

            db = db_session_factory()
            audit = AuditEvent(
                id=str(uuid.uuid4()),
                execution_id=event["execution_id"],
                event_type=event["event_type"],
                timestamp=datetime.now(timezone.utc),
                actor=event.get("actor", "system"),
                event_metadata=event.get("metadata", "")
            )
            db.add(audit)
            db.commit()
            db.close()

            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Event processed and saved to DB")

        except Exception as e:
            print(f"Consumer error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def run():
        try:
            connection = get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback
            )
            print("RabbitMQ consumer started — waiting for events...")
            channel.start_consuming()
        except Exception as e:
            print(f"Consumer connection error: {e}")

    # Run consumer in background thread
    thread = threading.Thread(target=run, daemon=True)
    thread.start()