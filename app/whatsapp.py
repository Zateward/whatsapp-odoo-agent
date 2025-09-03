from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Tus credenciales de Twilio
account_sid = os.getenv("twilio_account_sid")
auth_token = os.getenv("twilio_auth_token")
client = Client(account_sid, auth_token)

# Número de WhatsApp del sandbox Twilio
whatsapp_twilio = "whatsapp:+14155238886"

# Tu número personal (registrado en el sandbox)
my_number = "whatsapp:+521..."

# Enviar mensaje
message = client.messages.create(
    from_=whatsapp_twilio,
    body="Hola este es un mensaje de prueba!",
    to=my_number
)

print(f"Message sent with SID: {message.sid}")