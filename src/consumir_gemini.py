"""
Módulo de consumo de servicios externos de IA (Google Gemini API).
Especialización en IA Accenture - Curso CCHIA
Unidad U1.3 · Bloque 6: Refactorización del script en funciones reutilizables
Actividad: Refactoriza tu script en un módulo del repositorio
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


def armar_peticion(pregunta: str):
    """
    Lee las credenciales, define el modelo y construye la URL y el cuerpo de la petición.
    Responsabilidad única: Preparación de parámetros y payload.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-3.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"

    body = {
        "contents": [
            {
                "parts": [{"text": pregunta}]
            }
        ]
    }

    return url, body


def enviar_peticion(url: str, body: dict, headers: dict = None) -> dict:
    """
    Envía la petición HTTP POST al servicio y devuelve la respuesta parseada a JSON.
    Responsabilidad única: Comunicación HTTP y deserialización.
    """
    respuesta = requests.post(url, headers=headers, json=body)
    return respuesta.json()


def extraer_texto(datos: dict) -> str:
    """
    Navega la estructura jerárquica de la respuesta JSON y extrae el texto generado.
    Responsabilidad única: Extracción del dato específico.
    """
    return datos["candidates"][0]["content"]["parts"][0]["text"]


def obtener_dato_de_prueba(pregunta: str) -> str:
    """
    Función coordinadora principal que orquesta el flujo completo delegando
    en las funciones especializadas: armar -> enviar -> extraer.
    Responsabilidad única: Orquestación del flujo y retorno del resultado.
    """
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)


if __name__ == "__main__":
    pregunta_prueba = "Confirma en una frase corta que esta conexión funciona correctamente."
    print(f"Pregunta enviada: {pregunta_prueba}\n")
    resultado = obtener_dato_de_prueba(pregunta_prueba)
    print("Respuesta generada por el modelo (funciones refactorizadas):")
    print(resultado)
