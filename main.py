from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from app.twilio_client import TwilioWhatsApp
from app.sales_agent import SalesAgent

app = FastAPI()
twilio = TwilioWhatsApp()
agent = SalesAgent()

@app.post("/webhook")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    print(f"📩 Mensaje recibido de {From}: {Body}")

    # Procesamos el mensaje con el agente de ventas
    reply = agent.handle_message(Body)
    print(f"🤖 Respuesta del agente: {reply}")

    # Respondemos por WhatsApp
    twilio.send_message(From, reply)

    # Twilio necesita algo en el webhook
    return PlainTextResponse("OK")
