from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from bson import ObjectId, errors
from app.queues.rabbitmq import RabbitMQ  
from flasgger import swag_from

notifications_bp = Blueprint('notifications', __name__)

mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client["test"]
users_collection = db.users
notifications_collection = db.notifications

rabbitmq = RabbitMQ()

@notifications_bp.route('/notifications', methods=['POST'])
@swag_from({
    'tags': ['Notifications'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'string', 'example': '68284a9f284eba457c65d0fb'},
                    'type': {'type': 'string', 'enum': ['email', 'sms', 'inapp'], 'example': 'email'},
                    'content': {'type': 'string', 'example': 'Hello, this is a test notification!'}
                },
                'required': ['user_id', 'type', 'content']
            }
        }
    ],
    'responses': {
        202: {
            'description': 'Notification queued',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'notification_id': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Invalid user_id format'},
        404: {'description': 'User not found'},
        500: {'description': 'Internal server error'}
    }
})

def send_notification():
    data = request.get_json(force=True)
    user_id = data.get('user_id')
    notification_type = data.get('type')
    content = data.get('content')

    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({'error': 'Invalid user_id format'}), 400

        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        notification_doc = {
            'user_id': user_id,
            'type': notification_type,
            'content': content,
            'status': 'pending',
            'email': user.get('email'),
            'phone': user.get('phone')
        }
        result = notifications_collection.insert_one(notification_doc)
        notif_id = str(result.inserted_id)

        rabbitmq.publish_message(notif_id)

        return jsonify({'message': 'Notification queued', 'notification_id': notif_id}), 202

    except errors.InvalidId:
        return jsonify({'error': 'Invalid user_id format'}), 400
    except Exception as e:
        print(f"Error in send_notification: {e}")
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/notifications/users/<user_id>/notifications', methods=['GET'])
@swag_from({
    'tags': ['Notifications'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'User ID',
            'default': '68284a9f284eba457c65d0fb'
        }
    ],
    'responses': {
        200: {
            'description': 'List of notifications for the user',
            'schema': {
                'type': 'object',
                'properties': {
                    'notifications': {
                        'type': 'array',
                        'items': {'type': 'object'}
                    }
                }
            }
        },
        400: {'description': 'Invalid user_id format'},
        500: {'description': 'Internal server error'}
    }
})

def get_user_notifications(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({'error': 'Invalid user_id format'}), 400

        docs = list(notifications_collection.find({'user_id': user_id}).sort('_id', -1))

        for doc in docs:
            doc['_id'] = str(doc['_id'])
            doc.pop('email', None)
            doc.pop('phone', None)

        return jsonify({'notifications': docs}), 200

    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
