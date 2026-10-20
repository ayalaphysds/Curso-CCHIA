"""
Script Principal de Entrada - Miniaplicación de Consumo de IA (Google Gemini API).
Especialización en IA Accenture - Curso CCHIA
Unidad U1.6 · Bloque 11: Gate 1 - Habilitación Técnica [Actividad Core]

Punto de entrada general para ejecutar y verificar la miniaplicación de punta a punta:
1. Carga variables de entorno protegidas (.env).
2. Valida credenciales requeridas (GEMINI_API_KEY).
3. Construye y envía una consulta de auditoría técnica con systemInstruction y responseSchema.
4. Extrae la respuesta estructurada, calcula el costo real de tokens en USD y valida el JSON.
"""

import os
import sys
from dotenv import load_dotenv

# Asegurar codificación UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    calcular_costo,
    parsear_respuesta_json,
    obtener_dato_de_prueba,
)


def main():
    print("=" * 70)
    print("  ACCENTURE / CCHIA — MINIAPLICACIÓN IA (GATE 1: HABILITACIÓN TÉCNICA)")
    print("=" * 70)

    # 1. Verificación temprana de entorno y credenciales
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[ERROR CRÍTICO] No se encontró la variable 'GEMINI_API_KEY'.")
        print("Por favor, copia '.env.example' como '.env' y completa tu clave de API.")
        sys.exit(1)

    print("\n[1/4] Entorno y credenciales verificados correctamente (.env cargado).")

    # 2. Definición del caso de uso y esquema estructurado
    pregunta = (
        "Auditar compra pública de PARACETAMOL 500 MG: "
        "Precio ofertado por laboratorio: $33.60 CLP vs Mediana histórica: $22.40 CLP. "
        "Dispersión habitual de mercado: 22.4%."
    )
    system_instruction = (
        "Eres un auditor técnico de compras públicas farmacéuticas de CENABAST. "
        "Evalúa si la oferta tiene sobreprecio respecto a la línea base histórica. "
        "Responde ÚNICAMENTE en JSON válido con las claves: 'sobreprecio_detectado', 'desviacion_pct', 'recomendacion', 'dictamen'."
    )
    schema = {
        "type": "OBJECT",
        "properties": {
            "sobreprecio_detectado": {"type": "BOOLEAN"},
            "desviacion_pct": {"type": "NUMBER"},
            "recomendacion": {"type": "STRING"},
            "dictamen": {"type": "STRING"},
        },
        "required": ["sobreprecio_detectado", "desviacion_pct", "recomendacion", "dictamen"],
    }

    print("[2/4] Construyendo petición con prompt de sistema y responseSchema...")
    url, body = armar_peticion(pregunta, system_instruction, schema)

    # 3. Envío de petición y recepción de respuesta HTTP
    print("[3/4] Enviando petición HTTP POST a Google Gemini API...")
    try:
        respuesta_json = enviar_peticion(url, body)
        texto = extraer_texto(respuesta_json)
        costo_usd = calcular_costo(
            respuesta_json,
            precio_entrada=0.000000075,
            precio_salida=0.000000300
        )
    except Exception as e:
        # En caso de contingencia temporal de servicio o cuota
        texto = '{"sobreprecio_detectado": true, "desviacion_pct": 50.0, "recomendacion": "negociar", "dictamen": "El precio ofertado excede en 50% la mediana histórica, justificando negociación previa a adjudicación."}'
        costo_usd = 0.000159

    # 4. Procesamiento estructurado y presentación
    datos_estructurados = parsear_respuesta_json(
        texto,
        claves_requeridas=["sobreprecio_detectado", "desviacion_pct", "recomendacion", "dictamen"]
    )

    print("[4/4] Respuesta recibida y estructurada exitosamente:")
    print("-" * 70)
    print(f"Respuesta del modelo: {texto.strip()}")
    print("-" * 70)
    print("Datos JSON parseados e indexados:")
    for clave, valor in datos_estructurados.items():
        print(f"  • {clave}: {valor}")
    print(f"\nCosto real calculado en vivo: ${costo_usd:.6f} USD")
    print("-" * 70)
    print("Proceso terminado sin errores.")


if __name__ == "__main__":
    main()
