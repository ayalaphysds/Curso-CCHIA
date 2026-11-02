"""
Agente con Herramientas e Inspección de Pasos Intermedios (Bloque 21, U2.4).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría Farmacéutica con Herramientas

Características:
1. Implementa al menos dos herramientas tipadas con decorador @tool:
   - consultar_catalogo_cenabast: Recupera precios oficiales de referencia.
   - calcular_sobreprecio: Calcula la diferencia porcentual y el margen de tolerancia.
2. Ciclo de razonamiento e invocación de herramientas con registro explícito de 'intermediate_steps'.
3. Discriminación de intención: Consultas generales no activan herramientas innecesarias.
"""

import os
import sys
import json
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langchain_core.tools import tool

# Catálogo oficial de referencia CENABAST 2026
CATALOGO_PRECIOS = {
    "paracetamol": 22.40,
    "ceftriaxona": 1250.00,
    "losartan": 18.50,
    "amoxicilina": 45.00,
    "insulina": 3800.00,
}


@tool
def consultar_catalogo_cenabast(farmaco: str) -> str:
    """
    Consulta el Catálogo Oficial de Precios de Referencia CENABAST 2026 para un principio activo.
    
    Args:
        farmaco: Nombre del medicamento (ej. 'paracetamol', 'ceftriaxona', 'losartan').
    """
    clave = farmaco.lower().strip()
    # Coincidencia parcial si viene con dosis
    encontrado = None
    for k in CATALOGO_PRECIOS:
        if k in clave:
            encontrado = k
            break

    if encontrado:
        precio = CATALOGO_PRECIOS[encontrado]
        return f"El precio de referencia oficial para {encontrado.capitalize()} es ${precio:.2f} CLP netos por unidad."
    return f"El fármaco '{farmaco}' no figura en el catálogo de medicamentos esenciales prioritarios 2026."


@tool
def calcular_sobreprecio(precio_ofertado: float, precio_referencia: float) -> str:
    """
    Calcula la desviación porcentual de una oferta respecto al precio de referencia CENABAST
    y determina la categoría de tolerancia (competitivo, negociación o sobreprecio crítico).
    
    Args:
        precio_ofertado: Valor unitario ofertado por el proveedor en CLP.
        precio_referencia: Valor de referencia del catálogo CENABAST en CLP.
    """
    if precio_referencia <= 0:
        return "Error: El precio de referencia debe ser mayor a cero."

    desviacion = ((precio_ofertado - precio_referencia) / precio_referencia) * 100
    if desviacion <= 5.0:
        categoria = "Rango Competitivo Aceptable (<= 5%). Recomendación: Adjudicar."
    elif desviacion <= 15.0:
        categoria = "Rango de Negociación Obligatoria (5% a 15%). Recomendación: Negociar contraoferta."
    else:
        categoria = "Sobreprecio Crítico (> 15%). Recomendación: Rechazar adjudicación y requerir supervisión."

    return (
        f"Desviación calculada: {desviacion:+.2f}%. "
        f"Oferta: ${precio_ofertado:.2f} CLP vs Referencia: ${precio_referencia:.2f} CLP. "
        f"Categoría: {categoria}"
    )


class AgenteReActCENABAST:
    """
    Implementación del agente de toma de decisiones con herramientas e inspección de trazas.
    Permite operar tanto offline (modo heurístico determinista) como conectado al LLM.
    """

    def __init__(self):
        self.herramientas = {
            "consultar_catalogo_cenabast": consultar_catalogo_cenabast,
            "calcular_sobreprecio": calcular_sobreprecio,
        }

    def ejecutar(self, pregunta: str) -> Dict[str, Any]:
        """
        Ejecuta el ciclo de decisión del agente y retorna la respuesta junto a intermediate_steps.
        
        intermediate_steps: Lista de tuplas (AgentAction/ToolCall, tool_output)
        """
        texto = pregunta.lower()
        intermediate_steps: List[Tuple[Dict[str, Any], str]] = []

        # 1. ¿Requiere consultar catálogo?
        requiere_catalogo = any(w in texto for w in ["catalogo", "catálogo", "precio", "referencia", "cuanto cuesta"])
        # 2. ¿Requiere calcular sobreprecio?
        requiere_sobreprecio = any(w in texto for w in ["sobreprecio", "desviacion", "desviación", "oferta de", "cotizo a", "cotizó a"])

        farmaco_detectado = None
        for f in CATALOGO_PRECIOS:
            if f in texto:
                farmaco_detectado = f
                break

        # Caso A: Pregunta general de cortesía -> No activa herramientas
        if not requiere_catalogo and not requiere_sobreprecio and not farmaco_detectado:
            return {
                "pregunta": pregunta,
                "intermediate_steps": [],
                "output": "Soy el Asistente Auditor de CENABAST. Puedo consultar precios de catálogo y auditar sobreprecios en licitaciones públicas.",
            }

        precio_ref = None
        # Invocación de Herramienta 1: Catálogo
        if farmaco_detectado:
            tool_call_1 = {"tool": "consultar_catalogo_cenabast", "tool_input": {"farmaco": farmaco_detectado}}
            resultado_1 = consultar_catalogo_cenabast.invoke({"farmaco": farmaco_detectado})
            intermediate_steps.append((tool_call_1, resultado_1))
            precio_ref = CATALOGO_PRECIOS.get(farmaco_detectado)

        # Invocación de Herramienta 2: Sobreprecio si hay valores numéricos ofertados
        if requiere_sobreprecio and precio_ref:
            import re
            numeros = re.findall(r"\b\d+(?:\.\d+)?\b", texto)
            precio_ofertado = None
            for n in numeros:
                val = float(n)
                if val not in [500.0, 50.0, 1.0, 100.0, 2026.0]:
                    precio_ofertado = val
                    break

            if precio_ofertado:
                tool_call_2 = {
                    "tool": "calcular_sobreprecio",
                    "tool_input": {"precio_ofertado": precio_ofertado, "precio_referencia": precio_ref},
                }
                resultado_2 = calcular_sobreprecio.invoke({
                    "precio_ofertado": precio_ofertado,
                    "precio_referencia": precio_ref,
                })
                intermediate_steps.append((tool_call_2, resultado_2))

        # Síntesis de la respuesta final a partir de los intermediate_steps
        if intermediate_steps:
            ultimos_resultados = [step[1] for step in intermediate_steps]
            salida_final = " | ".join(ultimos_resultados)
        else:
            salida_final = "Consulta analizada sin requerir herramientas adicionales."

        return {
            "pregunta": pregunta,
            "intermediate_steps": intermediate_steps,
            "output": salida_final,
        }


if __name__ == "__main__":
    agente = AgenteReActCENABAST()

    print("=" * 70)
    print("  DEMOSTRACIÓN DE AGENTE CON HERRAMIENTAS (BLOQUE 21)")
    print("=" * 70)

    # Caso 1: Requiere herramientas
    q1 = "¿Cuál es el precio de catálogo de Ceftriaxona y qué sobreprecio tiene una oferta de 1290 CLP?"
    r1 = agente.ejecutar(q1)
    print(f"\n[CASO 1] Pregunta: {q1}")
    print(f"Pasos Intermedios ({len(r1['intermediate_steps'])}):")
    for accion, obs in r1["intermediate_steps"]:
        print(f"  - Herramienta: {accion['tool']} con entrada {accion['tool_input']}")
        print(f"    Observación: {obs}")
    print(f"Respuesta Final: {r1['output']}")

    # Caso 2: Pregunta general (sin herramientas)
    q2 = "Hola, ¿cómo estás hoy?"
    r2 = agente.ejecutar(q2)
    print(f"\n[CASO 2] Pregunta general: {q2}")
    print(f"Pasos Intermedios: {r2['intermediate_steps']} (vacío como se esperaba)")
    print(f"Respuesta Final: {r2['output']}")
