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

    # 1. Intentar procesar con el agente de concurso
    reply = contest_agent.handle_message(From, Body)

    # 2. Si no es concurso, usar el agente de ventas
    if not reply:
        reply = sales_agent.handle_message(Body)

    print(f"🤖 Respuesta del agente: {reply}")

    # 3. Enviar la respuesta SOLO una vez
    try:
        sid = twilio.send_message(From, reply)
        print(f"✅ Mensaje enviado con SID: {sid}")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

    return PlainTextResponse("OK")