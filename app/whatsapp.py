from twilio.rest import Client
from dotenv import load_dotenv
import os

class TwilioWhatsApp:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv("twilio_account_sid")
        self.auth_token = os.getenv("twilio_auth_token")
        self.client = Client(self.account_sid, self.auth_token)

        self.whatsapp_twilio = os.getenv("twilio_whatsapp_number", "whatsapp:+14155238886")  # Sandbox por defecto

    def send_message(self, to_number, message_body):
        # Enviar mensaje
        message = self.client.messages.create(
            from_=self.whatsapp_twilio,
            body=message_body,
            to=to_number
        )
        return message.sid

load_dotenv()

# Tus credenciales de Twilio
account_sid = os.getenv("twilio_account_sid")
auth_token = os.getenv("twilio_auth_token")
client = Client(account_sid, auth_token)

# Número de WhatsApp del sandbox Twilio
whatsapp_twilio = "whatsapp:+14155238886"

# Tu número personal (registrado en el sandbox)
my_number = "whatsapp:+5215566738374"

# Enviar mensaje
message = client.messages.create(
    from_=whatsapp_twilio,
    body="Hola este es un mensaje de prueba!",
    to=my_number
)

print(f"Message sent with SID: {message.sid}")