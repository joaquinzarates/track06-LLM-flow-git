import json
import time
import google.genai as genai
from config import GEMINI_API_KEY, MODELO, MAX_TOKENS

def cargar_prompt_sistema():
    with open("prompts/system_revisor.txt", "r", encoding="utf-8") as f:
        return f.read()

def dividir_diff_por_archivo(diff):
    archivos = []
    actual = []
    for linea in diff.splitlines(keepends=True):
        if linea.startswith("diff --git") and actual:
            archivos.append("".join(actual))
            actual = []
        actual.append(linea)
    if actual:
        archivos.append("".join(actual))
    return archivos

def revisar_diff(diff):
    genai.configure(api_key=GEMINI_API_KEY)
    modelo = genai.GenerativeModel(
        model_name=MODELO,
        system_instruction=cargar_prompt_sistema()
    )

    fragmentos = dividir_diff_por_archivo(diff)
    todos_hallazgos = []
    resumen_partes = []

    for fragmento in fragmentos:
        resultado = _llamar_modelo_con_reintento(modelo, fragmento)
        if resultado:
            todos_hallazgos.extend(resultado.get("hallazgos", []))
            resumen_partes.append(resultado.get("resumen", ""))

    return {
        "resumen": " ".join(resumen_partes),
        "total_hallazgos": len(todos_hallazgos),
        "hallazgos": todos_hallazgos
    }

def _llamar_modelo_con_reintento(modelo, diff, intentos=3):
    for intento in range(intentos):
        try:
            respuesta = modelo.generate_content(
                f"Analiza el siguiente diff:\n\n{diff}",
                generation_config={"max_output_tokens": MAX_TOKENS}
            )
            return _validar_respuesta(respuesta.text)
        except Exception as e:
            if intento < intentos - 1:
                time.sleep(2 ** intento)
            else:
                print(f"Error tras {intentos} intentos: {e}")
                return None

def _validar_respuesta(texto):
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.split("\n", 1)[-1]
        texto = texto.rsplit("```", 1)[0]
    try:
        datos = json.loads(texto)
        assert "hallazgos" in datos
        assert "total_hallazgos" in datos
        return datos
    except (json.JSONDecodeError, AssertionError):
        print("Respuesta del LLM con formato inesperado.")
        return None