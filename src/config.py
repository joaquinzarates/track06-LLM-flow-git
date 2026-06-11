import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = "gemini-2.5-flash"
MAX_TOKENS = 8192

def validar_configuracion():
    if not GEMINI_API_KEY:
        raise ValueError(
            "No se encontró la API - Key de Gemini. "
            "Verifica que el archivo .env existe y contiene la key."
        )