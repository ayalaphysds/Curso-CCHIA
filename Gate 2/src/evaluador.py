"""
Módulo Evaluador de Calidad de Recuperación, Citas y Telemetría (Bloque 27 y 28, U2.5).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría Cuantitativa de Desempeño RAG

Métricas calculadas:
1. Precisión documental: proporción de chunks relevantes recuperados.
2. Cobertura de citas: verificación textual de que las fuentes recuperadas aparecen citadas en la respuesta.
3. Telemetría de latencia: tiempo total de procesamiento en milisegundos.
4. Estimación de costos: costo operacional según tarifas por cada 1.000 tokens.
"""

from typing import List, Dict, Any, Set
from langchain_core.documents import Document


def calcular_metricas_recuperacion(
    recuperados: List[Document],
    fuentes_esperadas: List[str]
) -> Dict[str, float]:
    """
    Calcula precisión y exhaustividad (recall) de las fuentes recuperadas
    frente a un conjunto esperado de documentos para la consulta.
    """
    if not recuperados or not fuentes_esperadas:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    fuentes_recuperadas: Set[str] = {
        doc.metadata.get("fuente") or doc.metadata.get("source") or ""
        for doc in recuperados
    }
    fuentes_recuperadas.discard("")

    esperadas_set = set(fuentes_esperadas)
    interseccion = fuentes_recuperadas.intersection(esperadas_set)

    precision = len(interseccion) / len(fuentes_recuperadas) if fuentes_recuperadas else 0.0
    recall = len(interseccion) / len(esperadas_set) if esperadas_set else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def verificar_citas_en_respuesta(respuesta: str, fuentes: List[str]) -> Dict[str, Any]:
    """
    Verifica si la respuesta generada incluye las fuentes con la sintaxis esperada
    [fuente: <nombre_archivo>] o mención explícita.
    """
    if not fuentes:
        return {"tiene_citas": False, "citas_encontradas": [], "cobertura": 0.0}

    citas_detectadas = [f for f in fuentes if f in respuesta]
    tiene_citas = len(citas_detectadas) > 0
    cobertura = len(citas_detectadas) / len(fuentes)

    return {
        "tiene_citas": tiene_citas,
        "citas_encontradas": citas_detectadas,
        "cobertura": round(cobertura, 4),
    }


def calcular_costo_y_latencia(
    duracion_ms: float,
    input_tokens: int,
    output_tokens: int,
    precio_1k_input_usd: float = 0.00015,
    precio_1k_output_usd: float = 0.00060,
    tipo_cambio_clp: float = 950.0
) -> Dict[str, float]:
    """
    Calcula la latencia y el costo estimado de la transacción.
    """
    costo_input = (input_tokens / 1000.0) * precio_1k_input_usd
    costo_output = (output_tokens / 1000.0) * precio_1k_output_usd
    costo_total_usd = costo_input + costo_output
    costo_total_clp = costo_total_usd * tipo_cambio_clp

    return {
        "duracion_ms": round(duracion_ms, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "costo_usd": round(costo_total_usd, 6),
        "costo_clp": round(costo_total_clp, 4),
    }
