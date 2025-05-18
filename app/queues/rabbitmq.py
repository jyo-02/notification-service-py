import os
import pika

class RabbitMQ:
    def __init__(self):
        self.url = os.getenv('RABBITMQ_URL')
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='notifications', durable=True)
        print("[RabbitMQ] Connected and queue declared")

    def publish_message(self, msg_id: str):
        self.channel.basic_publish(
            exchange='',
            routing_key='notifications',
            body=msg_id,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"[RabbitMQ] Published {msg_id}")

    def consume(self, callback):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='notifications',
            on_message_callback=callback,
            auto_ack=False
        )
        print("[RabbitMQ] Waiting for messages…")
        self.channel.start_consuming()
