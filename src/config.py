import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = "gemini-2.5-flash"
MAX_TOKENS = 8192

def validar_configuracion():
    if not GEMINI_API_KEY:
        raise ValueError(
            "No se encontró GEMINI_API_KEY. "
            "Verifica que el archivo .env existe y contiene la key."
        )