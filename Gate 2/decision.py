"""
Matriz Cuantitativa de Decisión de Personalización: RAG vs PEFT vs Fine-Tuning (Bloque 30, U2.6).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría de Adquisiciones de Medicamentos

Este script:
1. Modela una matriz de decisión cuantitativa con ponderaciones y puntuaciones [1 a 5].
2. Evalúa las tres arquitecturas de personalización para el dominio CENABAST:
   - RAG (Retrieval-Augmented Generation con Vector Store)
   - PEFT (Parameter-Efficient Fine-Tuning: LoRA, QLoRA, Prefix Tuning)
   - Full Fine-Tuning (Ajuste Fino Completo de Pesos)
3. Ejecuta el algoritmo de recomendación fundamentada.
4. Genera el informe cuantitativo que respalda el Architecture Decision Record (ADR).
"""

import os
import sys
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# -----------------------------------------------------------------------------
# 1. Dimensiones Ponderadas de Decisión de Arquitectura
# -----------------------------------------------------------------------------
CRITERIOS_DECISION = [
    {
        "id": "dinamismo_info",
        "nombre": "Dinamismo de la Información (Frecuencia de cambios de precios/normas)",
        "peso": 0.25,
        "descripcion": "Los precios de catálogo y bases de licitación cambian mensual y trimestralmente."
    },
    {
        "id": "auditabilidad_citas",
        "nombre": "Auditabilidad y Citación Estricta de Fuentes",
        "peso": 0.25,
        "descripcion": "Exigencia legal de respaldo mediante citas explícitas del documento oficial."
    },
    {
        "id": "control_alucinaciones",
        "nombre": "Control de Alucinaciones en Datos Numéricos y Moneda",
        "peso": 0.20,
        "descripcion": "Tolerancia cero a inventar valores de medicamentos esenciales."
    },
    {
        "id": "costo_mantenimiento",
        "nombre": "Eficiencia en Costo de Cómputo y Mantenimiento",
        "peso": 0.15,
        "descripcion": "Costo de re-entrenamiento versus re-indexación ligera en disco."
    },
    {
        "id": "disponibilidad_datos",
        "nombre": "Volumen de Datos de Entrenamiento Etiquetados",
        "peso": 0.15,
        "descripcion": "Disponibilidad de miles de pares prompt-completado específicos de compras públicas."
    }
]

# Puntuaciones objetivas por técnica en escala 1 a 5 (5 = Excelente / Óptimo, 1 = Deficiente / Inviable)
PUNTAJES_TECNICAS = {
    "RAG": {
        "dinamismo_info": 5.0,        # Actualizar índice en segundos sin reentrenamiento
        "auditabilidad_citas": 5.0,   # Cita exacta con metadata del chunk recuperado
        "control_alucinaciones": 4.5, # Anclado estrictamente al contexto recuperado
        "costo_mantenimiento": 5.0,   # Costo marginal casi nulo de almacenamiento vectorial
        "disponibilidad_datos": 5.0,  # No requiere dataset masivo supervisado; opera con docs markdown
    },
    "PEFT_LoRA": {
        "dinamismo_info": 2.0,        # Exige reentrenar adaptadores cada vez que cambia un precio
        "auditabilidad_citas": 2.5,   # No almacena punteros directos a archivos fuente
        "control_alucinaciones": 3.0, # Riesgo de alucinación paramétrica de cifras
        "costo_mantenimiento": 4.0,   # Cómputo moderado (entrena <1% de parámetros)
        "disponibilidad_datos": 3.0,  # Requiere cientos o miles de ejemplos curados
    },
    "Full_FineTuning": {
        "dinamismo_info": 1.0,        # Completamente inviable para datos volátiles de precios
        "auditabilidad_citas": 2.0,   # Caja negra en cuanto a procedencia de cada número
        "control_alucinaciones": 2.5, # Alto riesgo de memorización distorsionada de precios
        "costo_mantenimiento": 1.5,   # Costos prohibitivos de GPUs (A100/H100)
        "disponibilidad_datos": 2.0,  # Requiere decenas de miles de ejemplos
    }
}


def calcular_evaluacion_cuantitativa() -> Dict[str, Any]:
    """Calcula el puntaje ponderado de cada técnica multiplicando peso por puntaje."""
    resultados = {}
    for tecnica, puntajes in PUNTAJES_TECNICAS.items():
        total_ponderado = 0.0
        desglose = {}
        for crit in CRITERIOS_DECISION:
            c_id = crit["id"]
            peso = crit["peso"]
            puntos = puntajes[c_id]
            subtotal = peso * puntos
            total_ponderado += subtotal
            desglose[c_id] = {
                "nombre": crit["nombre"],
                "peso": peso,
                "puntos": puntos,
                "subtotal_ponderado": round(subtotal, 3)
            }
        resultados[tecnica] = {
            "puntaje_final": round(total_ponderado, 3),
            "desglose": desglose
        }
    return resultados


def recomendar_estrategia(evaluacion: Dict[str, Any]) -> Dict[str, Any]:
    """Determina la técnica ganadora y genera la justificación técnica."""
    tecnica_ganadora = max(evaluacion.items(), key=lambda x: x[1]["puntaje_final"])
    nombre_ganador = tecnica_ganadora[0]
    puntaje = tecnica_ganadora[1]["puntaje_final"]

    justificacion = (
        f"La arquitectura óptima para CENABAST es {nombre_ganador} con un puntaje de {puntaje}/5.000. "
        "Razones determinantes: 1) Los precios de medicamentos y regulaciones sufren variaciones mensuales, "
        "lo cual vuelve inviable económicamente el re-entrenamiento continuo de pesos; 2) La normativa de compras "
        "públicas exige citación formal e incontrovertible del documento fuente, cualidad nativa de RAG; y 3) "
        "RAG previene alucinaciones numéricas al forzar el anclaje del LLM en el catálogo oficial 2026."
    )

    return {
        "estrategia_recomendada": nombre_ganador,
        "puntaje_ganador": puntaje,
        "ranking": sorted(
            [{"tecnica": k, "puntaje": v["puntaje_final"]} for k, v in evaluacion.items()],
            key=lambda x: x["puntaje"],
            reverse=True
        ),
        "justificacion": justificacion
    }


def main():
    print("=" * 75)
    print("  MATRIZ CUANTITATIVA DE DECISIÓN DE ARQUITECTURA (BLOQUE 30)")
    print("=" * 75)

    evaluacion = calcular_evaluacion_cuantitativa()
    recomendacion = recomendar_estrategia(evaluacion)

    print("\nRESUMEN PONDERADO DE TÉCNICAS (Escala 1.0 - 5.0):")
    for item in recomendacion["ranking"]:
        print(f"  • {item['tecnica']:<16}: {item['puntaje']:.3f} puntos")

    print("\nRECOMENDACIÓN FINAL FUNDAMENTADA:")
    print(f"  Estrategia Seleccionada: {recomendacion['estrategia_recomendada']}")
    print(f"  Dictamen de Ingeniería:\n    {recomendacion['justificacion']}")


if __name__ == "__main__":
    main()
