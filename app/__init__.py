from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['RABBITMQ_URL'] = os.getenv('RABBITMQ_URL')
    app.config['SMTP_SERVER'] = os.getenv('SMTP_SERVER')
    app.config['SMTP_PORT'] = os.getenv('SMTP_PORT')
    app.config['SMTP_USER'] = os.getenv('SMTP_USER')
    app.config['SMTP_PASSWORD'] = os.getenv('SMTP_PASSWORD')
    app.config['TWILIO_SID'] = os.getenv('TWILIO_SID')
    app.config['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN')
    app.config['TWILIO_PHONE_FROM'] = os.getenv('TWILIO_PHONE_FROM')

    from .routes.notifications import notifications_bp
    app.register_blueprint(notifications_bp)

    return app 