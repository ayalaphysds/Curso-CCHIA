"""
Módulo de consumo de servicios externos de IA (Google Gemini API).
Especialización en IA Accenture - Curso CCHIA
Unidad U1.3 · Bloque 5: Primer módulo Python que consume un servicio externo
Actividad práctica: Construye tu módulo Python de consumo de servicios
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Asegurar codificación UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def obtener_dato_de_prueba(pregunta: str) -> str:
    """
    Envía una pregunta o instrucción a la API de Google Gemini y devuelve el texto generado.
    
    Responsabilidad única: recibe el dato de entrada, realiza la petición HTTP,
    parsea la respuesta JSON y extrae el texto generado devolviéndolo con return.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-3.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    body = {
        "contents": [
            {
                "parts": [
                    {"text": pregunta}
                ]
            }
        ]
    }

    respuesta = requests.post(url, headers=headers, json=body)
    datos = respuesta.json()

    # Extraer el texto generado desde la estructura jerárquica de Gemini:
    # candidates -> 0 -> content -> parts -> 0 -> text
    return datos["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    pregunta_prueba = "Confirma en una frase corta que esta conexión funciona correctamente."
    print(f"Pregunta enviada: {pregunta_prueba}\n")
    resultado = obtener_dato_de_prueba(pregunta_prueba)
    print("Respuesta generada por el modelo:")
    print(resultado)
