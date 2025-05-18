import threading
import time
import os
from flask import Flask
from flasgger import Swagger
from app.routes.notifications import notifications_bp
from worker import process_notification, rabbitmq  # Worker logic

def create_app():
    app = Flask(__name__)
    app.register_blueprint(notifications_bp)
    app.config['SWAGGER'] = {
        'title': 'Notification Service API',
        'uiversion': 3
    }
    Swagger(app)
    return app

app = create_app()

def start_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False, use_reloader=False)

def start_worker():
    print("[Main] Starting worker thread...")
    try:
        rabbitmq.consume(process_notification)
    except KeyboardInterrupt:
        print("[Main] Worker stopped.")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    worker_thread = threading.Thread(target=start_worker)

    flask_thread.start()
    #slight delay for flask to start
    time.sleep(2)
    worker_thread.start()

    flask_thread.join()
    worker_thread.join() 