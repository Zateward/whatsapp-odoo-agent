from .gemini_client import GeminiClient
from .odoo_client import OdooClient

class SalesAgent:
    def __init__(self):
        self.gemini = GeminiClient()
        self.odoo = OdooClient()

    def handle_message(self, message: str):
        """
        1. Analiza el mensaje del cliente
        2. Consulta Odoo si se necesita info de productos
        3. Genera respuesta con Gemini
        """
        response_text = ""

        # Ejemplo: si el mensaje contiene "producto" o "precio", buscamos en Odoo
        if "precio" in message.lower() or "producto" in message.lower() or "buscando" in message.lower():
            products = self.odoo.search_read_products()
            # Generamos un texto breve con los productos
            products_text = "\n".join(
                [f"{p['name']}: (Precio: {p['list_price']})" for p in products[:10]]
            )
            prompt = f"""Actúa como agente de ventas para la empresa Technodomus, tu te llamas Anastasio Loqueron.
            Cliente pregunta: '{message}'. Aquí están algunos productos disponibles con el precio en pesos mexicanos:\n{products_text}\n
            Responde de manera amigable y profesional. La respuesta no debe exceder los 1500 caracteres."""
            response_text = self.gemini.get_response(prompt)
        else:
            # Mensajes generales → IA responde normalmente
            prompt = f"Actúa como un agente de ventas experto en equipo biomédico. Cliente dice: '{message}'"
            response_text = self.gemini.get_response(prompt)

        return response_text
