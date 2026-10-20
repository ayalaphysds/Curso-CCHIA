"""
Módulo de consumo de servicios externos de IA (Google Gemini API).
Especialización en IA Accenture - Curso CCHIA
Unidad U1.3 · Bloque 7: Manejo de excepciones y validación de entradas [Actividad Core]

Rúbrica de Calidad de Código:
- Responsabilidad única: cada función se encarga de un solo paso y de su propia validación/error.
- Nombres descriptivos: nombres claros y autoexplicativos.
- Comportamiento correcto y verificado: preserva el comportamiento ante entradas válidas.
- Manejo adecuado de errores: excepciones específicas con mensajes claros y accionables.
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


def armar_peticion(pregunta: str) -> tuple[str, dict]:
    """
    Valida la entrada, lee las credenciales y prepara la URL y el cuerpo de la petición.
    
    Responsabilidad única: Validación temprana y preparación de parámetros.
    Lanza:
        ValueError: Si la pregunta está vacía, no es texto o contiene solo espacios en blanco.
    """
    if not pregunta or not isinstance(pregunta, str) or not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía")

    api_key = os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"

    body = {
        "contents": [
            {
                "parts": [{"text": pregunta.strip()}]
            }
        ]
    }

    return url, body


def enviar_peticion(url: str, body: dict, headers: dict = None) -> dict:
    """
    Envía la petición HTTP POST al servicio externo y deserializa la respuesta JSON.
    
    Responsabilidad única: Comunicación de red y conversión a JSON.
    Lanza:
        RuntimeError: Si ocurre un fallo de conexión o si la respuesta no es un JSON válido.
    """
    try:
        respuesta = requests.post(url, headers=headers, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio tardó demasiado tiempo en responder (timeout).")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de red al consultar el servicio: {e}")

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")


def extraer_texto(datos: dict) -> str:
    """
    Navega la estructura jerárquica de la respuesta JSON y extrae el texto generado.
    
    Responsabilidad única: Extracción de datos específicos de la respuesta.
    Lanza:
        RuntimeError: Si la respuesta no contiene la estructura o claves esperadas ('candidates').
    """
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")


def calcular_costo(datos: dict, precio_entrada: float, precio_salida: float) -> float:
    """
    Calcula el costo monetario real (USD) de una petición a partir del bloque 'usageMetadata'.
    
    Responsabilidad única: Cálculo de costo a partir del conteo de tokens.
    Lanza:
        RuntimeError: Si la respuesta no contiene 'usageMetadata' o la estructura esperada.
    """
    try:
        uso = datos["usageMetadata"]
        tokens_entrada = uso["promptTokenCount"]
        tokens_salida = uso["candidatesTokenCount"]
        return (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida)
    except (KeyError, TypeError):
        raise RuntimeError("La respuesta no contiene los metadatos de uso ('usageMetadata') esperados.")



def obtener_dato_de_prueba(pregunta: str) -> str:
    """
    Función coordinadora principal que orquesta el flujo completo de consulta a la IA:
    armar_peticion -> enviar_peticion -> extraer_texto.
    
    Responsabilidad única: Coordinación del flujo y retorno del dato limpio.
    """
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)


if __name__ == "__main__":
    print("=" * 70)
    print("  ACCENTURE / CCHIA - U1.3 BLOQUE 7: EXCEPCIONES Y VALIDACIÓN")
    print("=" * 70)

    # 1. Prueba de validación de entrada vacía
    print("\n[PRUEBA 1] Validación de entrada vacía:")
    try:
        obtener_dato_de_prueba("")
    except ValueError as error:
        print(f"  ✓ Error de validación capturado exitosamente: {error}")
    except Exception as error:
        print(f"  ✗ Error inesperado: {error}")

    # 2. Prueba de fallo de conexión de red
    print("\n[PRUEBA 2] Fallo de conexión de red inducido:")
    try:
        enviar_peticion("https://esta-direccion-no-existe.ejemplo/datos", {})
    except RuntimeError as error:
        print(f"  ✓ Error de conexión contenido exitosamente: {error}")
    except Exception as error:
        print(f"  ✗ Error inesperado: {error}")

    # 3. Prueba de formato de respuesta o dato faltante
    print("\n[PRUEBA 3] Respuesta sin estructura esperada (dato faltante):")
    try:
        extraer_texto({"respuesta_invalida": True})
    except RuntimeError as error:
        print(f"  ✓ Error de dato faltante contenido exitosamente: {error}")
    except Exception as error:
        print(f"  ✗ Error inesperado: {error}")

    # 4. Prueba del camino exitoso (Happy Path)
    print("\n[PRUEBA 4] Camino exitoso (Consulta válida a Gemini API):")
    pregunta_valida = "Confirma en una frase corta que esta conexión funciona correctamente."
    try:
        resultado = obtener_dato_de_prueba(pregunta_valida)
        print("  ✓ Respuesta generada por el modelo:")
        print(f"    \"{resultado.strip()}\"")
    except (ValueError, RuntimeError) as error:
        print(f"  ✗ No se pudo completar la operación: {error}")

    print("\n" + "=" * 70)
    print("  Todas las pruebas de la rúbrica ejecutadas sin caídas abruptas.")
    print("=" * 70)
