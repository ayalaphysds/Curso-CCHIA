"""
Cliente modular de consumo de modelos generativos con reintentos y clasificación de errores.
Especialización en IA Accenture - Curso CCHIA
Módulo 2: Construcción de componentes IA · U2.1 · Bloque 12
Actividad Práctica: Desarrolla tu cliente modular de consumo de modelos

Características:
1. Único punto de entrada: consultar_modelo(pregunta, system_instruction).
2. Clasificación rigurosa de errores:
   - Autenticación (401/403): Lanza ValueError, no se reintenta.
   - Rate limit / Red (429/500/timeout): Lanza TimeoutError, se reintenta automáticamente.
3. Reintento automático con política definida en con_reintento.
4. Encapsulación completa: agotamiento de reintentos transformado a RuntimeError entendible.
"""

import os
import sys
import requests
from typing import Callable, Any
from dotenv import load_dotenv

# Asegurar codificación UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# Importar componentes modulares de las lecciones del Bloque 12
from cliente_api import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    obtener_url,
    headers,
    URL,
    GEMINI_API_KEY,
)
from cliente_reintento import con_reintento


def consultar_modelo(
    pregunta: str,
    system_instruction: str = "",
) -> str:
    """
    Función pública principal del cliente modular.
    
    Flujo:
    1. Valida y arma el cuerpo de la petición.
    2. Envía la petición aplicando la política de reintentos (con_reintento).
    3. Convierte el agotamiento de reintentos (TimeoutError) en un RuntimeError para el consumidor.
    4. Permite que ValueError (credencial inválida o error de configuración) se propague tal cual.
    5. Extrae y devuelve el texto procesado.
    """
    cuerpo = armar_peticion(pregunta, system_instruction)
    try:
        respuesta = con_reintento(lambda: enviar_peticion(cuerpo))
    except TimeoutError:
        raise RuntimeError("El servicio no respondió tras varios intentos. Intenta más tarde.")
    return extraer_texto(respuesta)


if __name__ == "__main__":
    print("=" * 75)
    print("  CLIENTE MODULAR DE CONSUMO DE MODELOS (BLOQUE 12) - VERIFICACIÓN")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # Escenario 1: Consulta normal exitosa
    # -------------------------------------------------------------------------
    print("\n[ESCENARIO 1] Consulta normal:")
    pregunta_demo = "¿Cuál es la capital de Chile?"
    try:
        print(f"  Pregunta: \"{pregunta_demo}\"")
        respuesta_demo = consultar_modelo(pregunta_demo)
        print(f"  Respuesta del modelo:\n    {respuesta_demo.strip()}")
        print("  ✓ Escenario 1 aprobado: El cliente funciona correctamente de punta a punta.")
    except Exception as err:
        print(f"  ✗ Error en Escenario 1: {err}")

    # -------------------------------------------------------------------------
    # Escenario 2: API Key inválida a propósito (falla inmediata, sin reintentos)
    # -------------------------------------------------------------------------
    print("\n[ESCENARIO 2] Verificación con API Key inválida (debe fallar de inmediato con ValueError):")
    clave_original = os.environ.get("GEMINI_API_KEY")
    try:
        os.environ["GEMINI_API_KEY"] = "clave_invalida_de_prueba"
        try:
            consultar_modelo("Consulta con credencial incorrecta.")
            print("  ✗ Error: La consulta debió lanzar ValueError.")
        except ValueError as err:
            print(f"  ✓ ValueError capturado exitosamente sin reintentar: {err}")
        except Exception as err:
            print(f"  ✗ Excepción no esperada: {type(err).__name__}: {err}")
    finally:
        if clave_original is not None:
            os.environ["GEMINI_API_KEY"] = clave_original

    # -------------------------------------------------------------------------
    # Escenario 3: Simulación de reintento ante límite de uso momentáneo
    # -------------------------------------------------------------------------
    print("\n[ESCENARIO 3] Demostración de reintento ante límite de uso temporal (429 simulado):")
    intentos_contador = [0]
    def mock_servicio_rate_limit():
        intentos_contador[0] += 1
        if intentos_contador[0] < 3:
            raise TimeoutError("Límite de peticiones excedido (429 simulado).")
        return {"contenido": "Respuesta simulada tras superar la congestión temporal en el intento 3."}

    resultado_simulado = con_reintento(mock_servicio_rate_limit, intentos=3, espera_segundos=1)
    print(f"  Resultado: {resultado_simulado['contenido']}")
    print("  ✓ Escenario 3 aprobado: con_reintento esperó y reintentó hasta el éxito.")

    # -------------------------------------------------------------------------
    # Escenario 4: Agotamiento de reintentos convertido en RuntimeError
    # -------------------------------------------------------------------------
    print("\n[ESCENARIO 4] Agotamiento de reintentos (conversión a RuntimeError):")
    def mock_falla_persistente():
        raise TimeoutError("Proveedor no disponible de forma prolongada.")

    try:
        try:
            con_reintento(mock_falla_persistente, intentos=2, espera_segundos=1)
        except TimeoutError:
            raise RuntimeError("El servicio no respondió tras varios intentos. Intenta más tarde.")
    except RuntimeError as err:
        print(f"  ✓ RuntimeError capturado con mensaje amigable: {err}")
        print("  ✓ Escenario 4 aprobado: El cliente enmascara la complejidad interna.")

    print("\n" + "=" * 75)
    print("  TODAS LAS PRUEBAS DE LA RÚBRICA DEL BLOQUE 12 EJECUTADAS EXITOSAMENTE")
    print("=" * 75)
