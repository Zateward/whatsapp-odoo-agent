# contest_agent.py
from .storage import save_user, load_users

class ContestAgent:
    def __init__(self):
        pass

    def handle_message(self, number, message):
        users = load_users()

        # 1. Si el mensaje es "join-technocontext", iniciamos registro
        if message.lower() == "join-technocontext":
            if number in users:
                return "Ya estás registrado! Gracias por tu participación!"
            else:
                # Creamos usuario temporal
                save_user(number, {"step": "awaiting_name"})
                return "¡Bienvenido al concurso! Para empezar escribe tu Nombre!"

        # 2. Si está en proceso de registro
        if number in users:
            user = users[number]
            step = user.get("step")

            if step == "awaiting_name":
                user["name"] = message
                user["step"] = "awaiting_company"
                save_user(number, user)
                return "Muchas gracias, cuentanos mas ¿y de qué empresa eres?"

            if step == "awaiting_company":
                user["company"] = message
                user["step"] = "awaiting_email"
                save_user(number, user)
                return "Genial, por último dime tu correo electrónico para acabar tu registro!"

            if step == "awaiting_email":
                user["email"] = message
                user["step"] = "awaiting_guess"
                save_user(number, user)
                return "¡Registro completo! Ahora la pregunta del millon, dime cuántas pelotas crees que hay en la lavadora."

            if step == "awaiting_guess":
                try:
                    guess = int(message)
                except ValueError:
                    return "Por favor indica un número válido."
                user["guess"] = guess
                user["step"] = "done"
                save_user(number, user)
                return f"¡Gracias {user['name']}! Tu predicción de {guess} pelotas ha sido registrada."

        # Mensajes fuera de flujo
        return "Para unirte al concurso, envía 'join-technocontext'."
