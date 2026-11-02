"""
Módulo de política y mecanismo de reintentos para consumo de APIs.
Especialización en IA Accenture - Curso CCHIA
Módulo 2: Construcción de componentes IA · U2.1 · Bloque 12
Lección 2: Reintento ante error del proveedor, construido en vivo
"""

import time
from typing import Callable, Any


def con_reintento(
    funcion: Callable[[], Any],
    intentos: int = 3,
    espera_segundos: int = 2,
) -> Any:
    """
    Envuelve una función y la reintenta automáticamente solo ante fallas temporales (TimeoutError).
    
    Parámetros:
        funcion: Invocable sin argumentos a ejecutar.
        intentos: Cantidad máxima de intentos permitidos (por defecto 3).
        espera_segundos: Pausa en segundos entre reintentos consecutivos (por defecto 2).
        
    Comportamiento:
        - Si la llamada es exitosa, devuelve inmediatamente su resultado.
        - Si captura TimeoutError y quedan intentos: imprime mensaje informativo y espera.
        - Si se agota el último intento (intento == intentos): re-lanza el TimeoutError original.
        - Si se produce cualquier otro error (como ValueError por auth), se propaga de inmediato sin reintentar.
    """
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except TimeoutError:
            if intento == intentos:
                raise
            print(f"Intento {intento} de {intentos} falló por límite de uso. Reintentando...")
            time.sleep(espera_segundos)
