# from fastapi import FastAPI, Form
# from fastapi.responses import PlainTextResponse
# from app.twilio_client import TwilioWhatsApp
# from app.sales_agent import SalesAgent

# app = FastAPI()
# twilio = TwilioWhatsApp()
# agent = SalesAgent()

# @app.post("/webhook")
# async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
#     print(f"📩 Mensaje recibido de {From}: {Body}")

#     # Procesamos el mensaje con el agente de ventas
#     reply = agent.handle_message(Body)
#     print(f"🤖 Respuesta del agente: {reply}")

#     # Respondemos por WhatsApp
#     twilio.send_message(From, reply)

#     # Twilio necesita algo en el webhook
#     return PlainTextResponse("OK")

from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from app.twilio_client import TwilioWhatsApp
from app.sales_agent import SalesAgent
from app.contest_agent import ContestAgent

app = FastAPI()
twilio = TwilioWhatsApp()
sales_agent = SalesAgent()
contest_agent = ContestAgent()

@app.post("/webhook")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    print(f"📩 Mensaje recibido de {From}: {Body}")

    # Asegurar que el número tiene el prefijo correcto
    if From.startswith("whatsapp:") and not From.startswith("whatsapp:+"):
        From = From.replace("whatsapp:", "whatsapp:+521", 1)

    reply = sales_agent.handle_message(Body)
    print(f"🤖 Respuesta del agente: {reply}")

    # Enviar la respuesta
    try:
        sid = twilio.send_message(From, reply)
        print(f"✅ Mensaje enviado con SID: {sid}")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

    return PlainTextResponse("OK")