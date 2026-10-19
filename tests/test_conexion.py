"""
Demostración de fragilidad ante errores de red y contención básica.
Especialización en IA Accenture - Curso CCHIA
Unidad U1.3 · Bloque 5: Primer módulo Python que consume un servicio externo
Lección 2: Un error de red a propósito, para aprender a manejarlo
"""

import requests


def obtener_datos(url: str):
    respuesta = requests.get(url, timeout=5)
    return respuesta.json()


def probar_error_inducido():
    url_rota = "https://esta-direccion-no-existe.ejemplo/datos"
    print("Probando petición a dirección inexistente (error de red inducido):")
    try:
        resultado = obtener_datos(url_rota)
        print("Resultado obtenido:", resultado)
    except requests.exceptions.RequestException as error:
        resultado = None
        print(f"No se pudo completar la petición (error contenido con éxito): {type(error).__name__}")


if __name__ == "__main__":
    probar_error_inducido()
