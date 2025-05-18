from twilio.rest import Client
import os

class SMSService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_number = os.getenv('TWILIO_PHONE_FROM')
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, to_number, message):
        #print(f"[SMSService] Sending SMS from {self.twilio_number} to {to_number}")

        self.client.messages.create(
            body=message,
            from_=self.twilio_number,
            to=to_number
        ) 