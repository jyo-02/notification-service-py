# Notification Service

A backend microservice for handling notifications  (**Email**, **SMS**, and **In-App**) using **Flask**, **MongoDB**, **RabbitMQ**, **Ethereal SMTP**, **Twilio**.

---

## 🚀 Features

* REST API to send and fetch notifications
* Notification types:

  * **Email** via [Ethereal](https://ethereal.email/)
  * **SMS** via [Twilio](https://www.twilio.com/)
  * **In-App** via a mocked Print to Console 
* Background job processing with **RabbitMQ**
* API documentation using **Swagger**

---

## 📦 Setup & Installation

### 1. Clone the Repository

```bash
git clone <repo-url>
cd notification-service
npm install
```

### 2. Configure Environment Variables

Create `.env` with the appropriate values:

```dotenv
# Server
PORT=5000

# MongoDB
MONGODB_URI=mongodb://localhost:27017/notifications

# RabbitMQ
RABBITMQ_URL=amqp://<user>:<pass>@<host>/<vhost>

# Ethereal SMTP
EMAIL_HOST=smtp.ethereal.email
EMAIL_PORT=587
EMAIL_USER=<your-ethereal-user>
EMAIL_PASS=<your-ethereal-pass>

# Twilio
TWILIO_SID=<your-twilio-sid>
TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
TWILIO_PHONE_NUMBER=+15551234567

```

### 3. Start Required Services

Make sure **MongoDB** and **RabbitMQ** are running locally or on the cloud.

### 4. Start the API Server

```bash
npm run dev
```

The server will start at `http://localhost:5000`

### 5. Start the Worker Process

```bash
npm run worker
```

---

## 📘 API Documentation & Testing

You can test all available endpoints using the live Swagger UI:

👉 **[https://notification-service-py.onrender.com/apidocs/](https://notification-service-py.onrender.com/apidocs/)**

Use the following sample user ID to test:

```json
{
  "userId": "68284a9f284eba457c65d0fb"
}
```

---

## 📡 API Endpoints

### ✅ Send Notification

* **POST** `/notifications`

**Sample Request Body:**

```json
{
  "userId": "68284a9f284eba457c65d0fb",
  "type": "sms",
  "content": "Hello from Swagger!"
}
```

### 📥 Get Notifications for a User

* **GET** `/notifications/users/{id}/notifications`

**Example Path Parameter:**

```
id = 68284a9f284eba457c65d0fb
```

---

## 📝 Notes

* **Email** notifications use [Ethereal](https://ethereal.email/) for testing. Use the Ethereal dashboard to view sent messages.
* **SMS** notifications are sent using [Twilio](https://www.twilio.com/). Ensure your credentials are valid.
* **In-App** notifications are mocked, printed to the console with simulated delay.
* Users must be added directly to the database — no registration or login endpoints are included in this service.
* For testing, use the sample `userId` provided above.

---
