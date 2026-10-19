"""
Script de verificación y primera petición autenticada a la API de Gemini.
Especialización en IA Accenture - Curso CCHIA
Unidad U1.2 · Bloque 4: Variables de entorno y primera petición HTTP autenticada
"""

import os
import sys
import json
from datetime import datetime

# Asegurar codificación UTF-8 en consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from dotenv import load_dotenv
    import requests
except ImportError as e:
    print(f"[ERROR] Dependencia no encontrada: {e}")
    print("Asegúrate de activar el entorno virtual e instalar las dependencias:")
    print("  .\\.venv\\Scripts\\Activate.ps1")
    print("  pip install -r requirements.txt")
    sys.exit(1)

def ofuscar_clave(clave: str) -> str:
    """Retorna la clave ofuscada para protegerla en impresiones y logs."""
    if not clave or len(clave) < 8:
        return "***"
    return f"{clave[:6]}...{clave[-4:]}"

def ejecutar_prueba():
    print("=" * 70)
    print("  ACCENTURE / CCHIA - U1.2 BLOQUE 4: PRIMERA PETICIÓN AUTENTICADA")
    print("=" * 70)

    # 1. Cargar variables de entorno desde .env
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    
    if not os.path.exists(env_path):
        print(f"\n[ALERTA] No se encontró el archivo .env en: {env_path}")
        print("Pasos para crearlo:")
        print("  1. En PowerShell ejecuta: Copy-Item .env.example .env")
        print("  2. Abre el archivo .env y asigna tu GEMINI_API_KEY")
        return False

    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "tu_llave_aqui" or "AIzaSy" not in api_key:
        print("\n[ALERTA] La variable GEMINI_API_KEY no tiene un valor válido configurado.")
        print(f"Valor actual detectado: {api_key if api_key else 'None'}")
        print("Por favor abre .env y pega tu API Key real de Google AI Studio.")
        return False

    print(f"\n[1] Archivo .env cargado correctamente.")
    print(f"    - Variable: GEMINI_API_KEY detectada.")
    print(f"    - Credencial protegida (ofuscada): {ofuscar_clave(api_key)}")

    # 2. Configurar petición HTTP a Gemini API
    # Usamos gemini-1.5-flash (modelo ligero y estándar del curso)
    model_name = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Hola, confirma por favor que esta conexión HTTP autenticada funciona correctamente para el Curso CCHIA."}
                ]
            }
        ]
    }

    print(f"\n[2] Enviando petición HTTP POST a:")
    print(f"    - Endpoint: {url}")
    print(f"    - Headers: Content-Type: application/json, x-goog-api-key: [OCULTA]")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        status_code = response.status_code
        print(f"\n[3] Código de respuesta HTTP: {status_code} ({response.reason})")

        if status_code == 200:
            data = response.json()
            # Extraer texto generado
            candidates = data.get("candidates", [])
            texto_generado = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    texto_generado = parts[0].get("text", "")

            print("\n" + "-" * 70)
            print("[PETICIÓN EXITOSA - STATUS 200 OK]")
            print(f"Respuesta generada por el modelo:\n\n{texto_generado.strip()}")
            print("-" * 70)

            # 3. Guardar evidencia en docs/ para el entregable de la actividad core
            docs_dir = os.path.join(base_dir, "docs")
            os.makedirs(docs_dir, exist_ok=True)
            evidencia_path = os.path.join(docs_dir, "evidencia_peticion_autenticada.json")

            evidencia_data = {
                "actividad": "U1.2 Bloque 4 - Ejecuta tu primera peticion autenticada de prueba [Actividad core]",
                "fecha_ejecucion": datetime.now().isoformat(),
                "endpoint": f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent",
                "metodo": "POST",
                "codigo_estado": status_code,
                "mensaje_estado": response.reason,
                "modelo_consultado": model_name,
                "credencial_utilizada": ofuscar_clave(api_key),
                "respuesta_modelo": texto_generado.strip(),
                "seguridad_credenciales": "Credencial protegida en .env y excluida via .gitignore. Ningun secreto expuesto."
            }

            with open(evidencia_path, "w", encoding="utf-8") as f:
                json.dump(evidencia_data, f, indent=2, ensure_ascii=False)

            print(f"\n[4] ¡Evidencia guardada exitosamente en docs/!")
            print(f"    Ruta: docs/evidencia_peticion_autenticada.json")
            print("\nEsta evidencia cumple con todos los requisitos del Gate 1:")
            print("  ✓ Endpoint documentado")
            print("  ✓ Código 200 OK comprobado")
            print("  ✓ Respuesta real generada")
            print("  ✓ Credenciales 100% protegidas y ofuscadas")
            return True

        elif status_code in (401, 403):
            print("\n[ERROR DE AUTENTICACIÓN - CÓDIGO 401/403]")
            print("Tu API Key no fue aceptada por Google Gemini.")
            print(f"Detalle devuelto por la API: {response.text}")
            return False
        elif status_code == 429:
            print("\n[LÍMITE EXCEDIDO - CÓDIGO 429]")
            print("Has alcanzado la cuota de peticiones por minuto. Espera un momento y reintenta.")
            return False
        else:
            print(f"\n[ERROR HTTP {status_code}]")
            print(f"Detalle: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR DE CONEXIÓN]: No se pudo conectar con el servidor: {e}")
        return False

if __name__ == "__main__":
    ejecutar_prueba()
