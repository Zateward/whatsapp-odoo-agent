from twilio.rest import Client
from dotenv import load_dotenv
import os

class TwilioWhatsApp:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv("twilio_account_sid")
        self.auth_token = os.getenv("twilio_auth_token")
        self.client = Client(self.account_sid, self.auth_token)
        self.whatsapp_twilio = "whatsapp:+14155238886"  # Sandbox

    def send_message(self, to_number: str, message_body: str):
        message = self.client.messages.create(
            from_=self.whatsapp_twilio,
            body=message_body,
            to=to_number
        )
        return message.sid
