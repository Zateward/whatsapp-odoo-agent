import google.generativeai as genai
from dotenv import load_dotenv
import os

class GeminiClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("gemini_api_key")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
