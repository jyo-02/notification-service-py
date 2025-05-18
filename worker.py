import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from app.services.in_app_service import InAppService
from app.queues.rabbitmq import RabbitMQ

load_dotenv()


def get_mongo_client():
    return MongoClient(os.getenv('MONGO_URI'))


email_service    = EmailService()
sms_service      = SMSService()
in_app_service   = InAppService()

rabbitmq = RabbitMQ() 

def get_notifications_collection():
    mongo_client = MongoClient(os.getenv('MONGO_URI'))
    db = mongo_client["test"]
    return db.notifications

def process_notification(ch, method, properties, body):
    from pymongo import MongoClient
    import os
    from bson.objectid import ObjectId
    from app.services.email_service import EmailService
    from app.services.sms_service import SMSService
    from app.services.in_app_service import InAppService

    try:
        print("[Worker] Received message from queue")
        mongo_uri = os.getenv('MONGO_URI')
        #print(f"[Worker] Using MONGO_URI: {mongo_uri}")
        mongo_client = MongoClient(mongo_uri)
        db = mongo_client["test"]
        notifications_collection = db.notifications

        notif_id = ObjectId(body.decode())
        notification = notifications_collection.find_one({'_id': notif_id})

        if not notification:
            print(f"[Worker] Notification not found: {notif_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        #print(f"[Worker] Notification: {notification}")

        typ = notification['type']
        email_service = EmailService()
        sms_service = SMSService()
        in_app_service = InAppService()

        if typ == 'email':
            email_service.send_email(notification['email'], 'Notification', notification['content'])
        elif typ == 'sms':
            sms_service.send_sms(notification['phone'], notification['content'])
        else:
            in_app_service.send_notification(notification['user_id'], notification['content'])

        notifications_collection.update_one(
            {'_id': notif_id},
            {'$set': {'status': 'sent'}}
        )
        print(f"[Worker] Notification sent and status updated: {notif_id}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[Worker][ERROR] Processing failed for {body}: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    print("[Worker] Starting to listen for notification jobs...")
    try:
        rabbitmq.consume(process_notification)
    except KeyboardInterrupt:
        print("\n[Worker] Stopping gracefully...")
        rabbitmq.channel.stop_consuming()
        rabbitmq.connection.close()
        print("[Worker] Shutdown complete.")