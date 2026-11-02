"""
Cadena de Tres Pasos para Auditoría de Compras Públicas CENABAST (Bloque 18, U2.3).
Especialización en IA Accenture - Curso CCHIA

Flujo encadenado LCEL (|) de tres etapas:
1. Paso 1 - Clasificación de Consulta:
   Identifica la naturaleza del requerimiento (Catálogo de Precios, Análisis de Sobreprecio o Abastecimiento/Riesgo).
2. Paso 2 - Análisis Técnico / Económico:
   Evalúa los parámetros cuantitativos o normativos relevantes para la solicitud.
3. Paso 3 - Formulación del Dictamen de Auditoría:
   Sintetiza la recomendación formal de compras públicas CENABAST.
"""

import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSerializable

# Catálogo local de referencia para soporte offline determinista
CATALOGO_PRECIOS = {
    "paracetamol": 22.40,
    "ceftriaxona": 1250.00,
    "losartan": 18.50,
    "amoxicilina": 45.00,
    "insulina": 3800.00,
}


def paso_1_clasificar(consulta: str) -> Dict[str, Any]:
    """Paso 1: Analiza la consulta y clasifica la categoría de auditoría."""
    texto = consulta.lower()
    if any(p in texto for p in ["sobreprecio", "oferta", "cotizacion", "cotización", "desviacion", "desviación"]):
        categoria = "sobreprecio"
    elif any(p in texto for p in ["catalogo", "catálogo", "precio", "mediana", "linea base", "línea base"]):
        categoria = "catalogo"
    elif any(p in texto for p in ["multa", "atraso", "quiebre", "stock", "abastecimiento", "plazo"]):
        categoria = "abastecimiento"
    else:
        categoria = "general"

    # Detección de fármaco mencionado
    farmaco_detectado = None
    for f in CATALOGO_PRECIOS.keys():
        if f in texto:
            farmaco_detectado = f
            break

    return {
        "consulta_original": consulta,
        "categoria": categoria,
        "farmaco": farmaco_detectado,
    }


def paso_2_analizar(estado: Dict[str, Any]) -> Dict[str, Any]:
    """Paso 2: Realiza el análisis técnico y económico según la categoría identificada."""
    categoria = estado["categoria"]
    farmaco = estado["farmaco"]
    consulta = estado["consulta_original"].lower()

    analisis = {}
    if categoria == "catalogo":
        if farmaco and farmaco in CATALOGO_PRECIOS:
            precio_ref = CATALOGO_PRECIOS[farmaco]
            analisis["detalle"] = f"El precio de referencia oficial para {farmaco.capitalize()} es de {precio_ref:.2f} CLP netos."
            analisis["precio_referencia"] = precio_ref
        else:
            analisis["detalle"] = "Consulta general de catálogo. Se debe consultar el listado oficial 2026 en data/cenabast_catalogo_precios_referencia_2026.md."

    elif categoria == "sobreprecio":
        # Extraer si hay un valor numérico ofertado
        import re
        numeros = re.findall(r"\b\d+(?:\.\d+)?\b", consulta)
        # Filtrar posibles números de dosis (500, 50, 100) y buscar precio
        precio_ofertado = None
        for n in numeros:
            val = float(n)
            if val not in [500.0, 50.0, 1.0, 100.0, 2026.0]:
                precio_ofertado = val
                break

        if farmaco and precio_ofertado and farmaco in CATALOGO_PRECIOS:
            ref = CATALOGO_PRECIOS[farmaco]
            desviacion = ((precio_ofertado - ref) / ref) * 100
            analisis["precio_ofertado"] = precio_ofertado
            analisis["precio_referencia"] = ref
            analisis["desviacion_pct"] = round(desviacion, 2)
            if desviacion <= 5.0:
                analisis["rango"] = "competitivo"
            elif desviacion <= 15.0:
                analisis["rango"] = "negociacion"
            else:
                analisis["rango"] = "sobreprecio_critico"
            analisis["detalle"] = f"Oferta: {precio_ofertado} CLP vs Ref: {ref} CLP. Desviación: {desviacion:+.2f}%."
        else:
            analisis["detalle"] = "Análisis de sobreprecio requiere especificar principio activo y precio unitario ofertado."

    elif categoria == "abastecimiento":
        analisis["detalle"] = "Normativa aplicable: Multa del 1% diario por atraso (máximo 15%). Quiebre potencial si el retraso excede 5 días en productos críticos."

    else:
        analisis["detalle"] = "Consulta general sin parámetros de cálculo específicos."

    estado["analisis"] = analisis
    return estado


def paso_3_dictamen(estado: Dict[str, Any]) -> str:
    """Paso 3: Emite el dictamen formal estructurado de auditoría CENABAST."""
    categoria = estado["categoria"]
    farmaco = estado.get("farmaco", "No especificado")
    analisis = estado.get("analisis", {})
    detalle = analisis.get("detalle", "")

    dictamen = [
        "============================================================",
        "  DICTAMEN DE AUDITORÍA DE COMPRAS PÚBLICAS - CENABAST",
        "============================================================",
        f"CATEGORÍA CLASIFICADA: {categoria.upper()}",
        f"FÁRMACO EVALUADO:      {farmaco.capitalize() if farmaco else 'N/A'}",
        f"ANÁLISIS TÉCNICO:      {detalle}",
    ]

    if "desviacion_pct" in analisis:
        desv = analisis["desviacion_pct"]
        rango = analisis["rango"]
        if rango == "competitivo":
            recomendacion = "RECOMENDAR ADJUDICACIÓN (Cumple margen competitivo <= 5%)."
        elif rango == "negociacion":
            recomendacion = "INICIAR NEGOCIACIÓN OBLIGATORIA (Desvío entre 5% y 15%)."
        else:
            recomendacion = "RECHAZAR ADJUDICACIÓN Y ACTIVAR SUPERVISIÓN HUMANA (Sobreprecio > 15%)."
        dictamen.append(f"RECOMENDACIÓN FORMAL:  {recomendacion}")
    elif categoria == "catalogo":
        dictamen.append("RECOMENDACIÓN FORMAL:  INFORMACIÓN VÁLIDA CONFORME AL CATÁLOGO BIENIO 2026.")
    elif categoria == "abastecimiento":
        dictamen.append("RECOMENDACIÓN FORMAL:  APLICAR SANCIONES Y MONITOREAR NIVEL DE CUMPLIMIENTO INCL.")
    else:
        dictamen.append("RECOMENDACIÓN FORMAL:  CONSULTA DERIVADA A MESA DE AYUDA DE ADQUISICIONES.")

    dictamen.append("============================================================")
    return "\n".join(dictamen)


def construir_cadena_tres_pasos():
    """
    Construye y retorna la cadena de 3 pasos conectada mediante LCEL:
    consulta_str | paso_1_clasificar | paso_2_analizar | paso_3_dictamen
    """
    cadena = (
        RunnableLambda(paso_1_clasificar)
        | RunnableLambda(paso_2_analizar)
        | RunnableLambda(paso_3_dictamen)
    )
    return cadena


if __name__ == "__main__":
    cadena = construir_cadena_tres_pasos()
    ejemplos = [
        "¿Cuál es el precio de catálogo de la Ceftriaxona?",
        "Auditar oferta de Paracetamol 500mg cotizada a 33.60 CLP",
        "¿Cuáles son las multas por atraso en el abastecimiento hospitalario?",
    ]
    for ej in ejemplos:
        print(f"\n>>> CONSULTA: {ej}")
        print(cadena.invoke(ej))
