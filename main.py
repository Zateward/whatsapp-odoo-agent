import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv
from twilio.request_validator import RequestValidator
from app.twilio_client import TwilioWhatsApp
from app.sales_agent import SalesAgent
from app.contest_agent import ContestAgent

# -------------------------
# Cargar variables desde .env
# -------------------------
load_dotenv()
TWILIO_AUTH_TOKEN = os.getenv("twilio_auth_token")
TWILIO_ACCOUNT_SID = os.getenv("twilio_account_sid")
TWILIO_WHATSAPP_NUMBER = os.getenv("twiliowhats_app_number")
META_VERIFY_TOKEN = os.getenv("meta_verify_token", "mi_token_seguro")  # opcional

# -------------------------
# Inicializar app y agentes
# -------------------------
app = FastAPI()
twilio = TwilioWhatsApp()
sales_agent = SalesAgent()
contest_agent = ContestAgent()

# -------------------------
# Meta webhook (opcional)
# -------------------------
@app.get("/webhook/meta")
async def verify_meta(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        return PlainTextResponse(challenge, status_code=200)
    return PlainTextResponse("Invalid token", status_code=403)


@app.post("/webhook/meta")
async def receive_meta(request: Request):
    data = await request.json()
    print("📩 Meta incoming:", data)
    return JSONResponse({"status": "ok"})


# -------------------------
# Función para validar Twilio
# -------------------------
async def validate_twilio_request(request: Request):
    """
    Valida que la petición venga realmente de Twilio
    usando la firma en el header X-Twilio-Signature.
    """
    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    url = str(request.url)
    form = await request.form()
    params = dict(form)
    signature = request.headers.get("X-Twilio-Signature", "")
    if not validator.validate(url, params, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    return params


# -------------------------
# Webhook de Twilio WhatsApp con agentes
# -------------------------
@app.post("/webhook/twilio")
async def receive_twilio(request: Request):
    # 1. Validar que venga de Twilio
    params = await validate_twilio_request(request)
    From = params.get("From")
    Body = params.get("Body")
    print(f"📩 Mensaje recibido de {From}: {Body}")

    # 2. Intentar procesar con el agente de concurso
    reply = contest_agent.handle_message(From, Body)

    # 3. Si no es concurso, usar el agente de ventas
    if not reply:
        reply = sales_agent.handle_message(Body)

    print(f"🤖 Respuesta del agente: {reply}")

    # 4. Enviar la respuesta SOLO una vez
    try:
        sid = twilio.send_message(From, reply)
        print(f"✅ Mensaje enviado con SID: {sid}")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

    return PlainTextResponse("OK")


# -------------------------
# Health check
# -------------------------
@app.get("/healthz")
async def health():
    return {"status": "running"}
