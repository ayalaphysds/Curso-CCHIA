"""
Módulo de cliente API para consumo de modelos generativos (Google Gemini API).
Especialización en IA Accenture - Curso CCHIA
Módulo 2: Construcción de componentes IA · U2.1 · Bloque 12
Lección 1: Un cliente que aguanta: autenticación y rate limits
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Asegurar codificación UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODELO}:generateContent?key={GEMINI_API_KEY}"
)
headers = {"Content-Type": "application/json"}


def obtener_url(api_key: str = None) -> str:
    """
    Construye dinámicamente la URL del endpoint con la API key vigente.
    Permite sobreescribir la credencial en caliente para pruebas o validaciones.
    """
    key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    return (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={key}"
    )


def armar_peticion(pregunta: str, system_instruction: str = "") -> dict:
    """
    Valida la entrada y prepara el cuerpo JSON de la petición para Gemini API.
    
    Lanza:
        ValueError: Si la pregunta está vacía o contiene solo espacios en blanco.
    """
    if not pregunta or not isinstance(pregunta, str) or not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía")

    cuerpo = {
        "contents": [
            {
                "parts": [{"text": pregunta.strip()}]
            }
        ]
    }
    if system_instruction:
        cuerpo["systemInstruction"] = {
            "parts": [{"text": system_instruction.strip()}]
        }
    return cuerpo


def enviar_peticion(cuerpo: dict) -> dict:
    """
    Envía la petición HTTP a la API y clasifica estrictamente las fallas:
    - 401 / 403 (o 400 API_KEY_INVALID): Falla de autenticación (ValueError, NO se debe reintentar).
    - 429 / >=500 / Timeout / ConnectionError: Falla temporal o rate limit (TimeoutError, SÍ se debe reintentar).
    """
    url_actual = obtener_url()
    try:
        respuesta = requests.post(
            url_actual, json=cuerpo, headers=headers, timeout=10
        )
    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ):
        raise TimeoutError("No se pudo contactar al proveedor. Puede ser momentáneo.")
    except requests.exceptions.RequestException as e:
        raise TimeoutError(f"Error de red al consultar el servicio: {e}")

    # Clasificación de errores según la rúbrica del Bloque 12
    if respuesta.status_code in (401, 403) or (
        respuesta.status_code == 400 and ("API_KEY_INVALID" in respuesta.text or "API key not valid" in respuesta.text)
    ):
        raise ValueError("Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY.")
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise TimeoutError("El proveedor no pudo procesar la petición. Hay que esperar y reintentar.")

    if hasattr(respuesta, "raise_for_status"):
        respuesta.raise_for_status()

    return respuesta.json()


def extraer_texto(respuesta: dict) -> str:
    """
    Extrae el texto generado por la API de Gemini o estructuras de respuesta simuladas.
    
    Lanza:
        RuntimeError: Si la estructura de la respuesta no contiene texto procesable.
    """
    if not isinstance(respuesta, dict):
        raise RuntimeError("La respuesta del servicio no es un diccionario válido.")

    if "candidates" in respuesta and respuesta["candidates"]:
        try:
            return respuesta["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            raise RuntimeError("La respuesta del servicio no contiene el texto esperado.")
    if "contenido" in respuesta:
        return str(respuesta["contenido"])
    if "texto" in respuesta:
        return str(respuesta["texto"])

    raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
