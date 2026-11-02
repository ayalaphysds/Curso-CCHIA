"""
Dataset de Ajuste Fino y Validación de Sintaxis para Personalización (Bloque 29, U2.6).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría de Compras Públicas Hospitalarias

Contenido:
1. Conjunto balanceado de 10 ejemplos en formato de instrucción (instruction, input, output).
   - 4 casos de Línea Base y Catálogo de Precios.
   - 3 casos de Análisis de Sobreprecio y Desviación Porcentual.
   - 3 casos de Gobernanza, Multas y Supervisión Humana.
2. Función de validación sintáctica y diagnóstico de balance 'validar_dataset'.
"""

import os
import sys
import json
from collections import Counter
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# -----------------------------------------------------------------------------
# 1. Dataset de 10 Ejemplos Estructurados para Personalización
# -----------------------------------------------------------------------------
DATASET_CENABAST: List[Dict[str, Any]] = [
    # Categoría 1: Catálogo y Línea Base de Precios (4 ejemplos)
    {
        "id": "CEN-TUNE-001",
        "categoria": "catalogo_precios",
        "instruction": "Identifica la mediana histórica oficial y forma farmacéutica para el Paracetamol en el catálogo CENABAST 2026.",
        "input": "Medicamento: Paracetamol 500 mg comprimidos.",
        "output": "Según el Catálogo Oficial 2026 de CENABAST, el Paracetamol 500 mg comprimido oral registra una mediana histórica de $22.40 CLP netos por unidad, con rango aceptable de $20.00 a $25.00 CLP."
    },
    {
        "id": "CEN-TUNE-002",
        "categoria": "catalogo_precios",
        "instruction": "Indica el valor de referencia institucional para la Ceftriaxona inyectable y sus requisitos técnicos.",
        "input": "Medicamento: Ceftriaxona 1 g frasco ampolla.",
        "output": "La Ceftriaxona 1 g inyectable tiene un precio de referencia de $1.250.00 CLP netos. Exige certificación de bioequivalencia del ISP y cadena de frío garantizada entre 2°C y 8°C hasta bodega de destino."
    },
    {
        "id": "CEN-TUNE-003",
        "categoria": "catalogo_precios",
        "instruction": "Proporciona la línea base de precio para Losartán potásico y su consumo estimado.",
        "input": "Medicamento: Losartán potásico 50 mg comprimidos recubiertos.",
        "output": "El Losartán potásico 50 mg comprimido presenta una mediana histórica de $18.50 CLP netos por unidad y un consumo anual proyectado de 88.000.000 de unidades en la red del SNSS."
    },
    {
        "id": "CEN-TUNE-004",
        "categoria": "catalogo_precios",
        "instruction": "Consulta el valor de referencia de Amoxicilina 500 mg y su presentación.",
        "input": "Medicamento: Amoxicilina 500 mg cápsulas.",
        "output": "La Amoxicilina 500 mg cápsulas registra una mediana histórica de $45.00 CLP netos por unidad según el catálogo de compras estratégicas CENABAST 2026."
    },

    # Categoría 2: Análisis de Sobreprecio y Desviación Porcentual (3 ejemplos)
    {
        "id": "CEN-TUNE-005",
        "categoria": "analisis_sobreprecio",
        "instruction": "Audita una oferta para Paracetamol 500 mg y emite dictamen conforme a los umbrales de sobreprecio.",
        "input": "Oferta recibida: $33.60 CLP unitario. Línea base: $22.40 CLP.",
        "output": "DICTAMEN: RECHAZAR ADJUDICACIÓN. La oferta presenta una desviación de +50.0% respecto a la mediana histórica ($22.40 CLP), superando con creces el umbral máximo de tolerancia (+15.0%). Califica como sobreprecio crítico lesivo al erario fiscal."
    },
    {
        "id": "CEN-TUNE-006",
        "categoria": "analisis_sobreprecio",
        "instruction": "Evalúa una oferta para Ceftriaxona 1 g y califica su admisibilidad económica.",
        "input": "Oferta recibida: $1.290.00 CLP unitario. Línea base: $1.250.00 CLP.",
        "output": "DICTAMEN: RECOMENDAR ADJUDICACIÓN. La oferta presenta una desviación de +3.2% respecto a la línea base de $1.250.00 CLP, situándose dentro del Rango Competitivo Aceptable (desviación <= 5.0%)."
    },
    {
        "id": "CEN-TUNE-007",
        "categoria": "analisis_sobreprecio",
        "instruction": "Dictamina la acción requerida ante una oferta en rango intermedio de sobreprecio para Losartán 50 mg.",
        "input": "Oferta recibida: $20.20 CLP unitario. Línea base: $18.50 CLP.",
        "output": "DICTAMEN: INICIAR NEGOCIACIÓN OBLIGATORIA. La oferta arroja una desviación de +9.19% sobre la referencia de $18.50 CLP, ubicándose en el tramo de negociación (5.0% a 15.0%). Corresponde solicitar contraoferta formal en Mercado Público antes de adjudicar."
    },

    # Categoría 3: Gobernanza, Multas y Supervisión Humana (3 ejemplos)
    {
        "id": "CEN-TUNE-008",
        "categoria": "gobernanza_y_riesgo",
        "instruction": "Explica la política de sanciones contractuales por atraso en la entrega de medicamentos.",
        "input": "Consulta sobre multas por atraso.",
        "output": "CENABAST aplica una multa del 1.0% diario sobre el valor neto de los bienes no entregados en plazo, con un tope máximo del 15.0% del total de la orden de compra. Cumplidos 15 días corridos de atraso, se faculta la rescisión unilateral del contrato."
    },
    {
        "id": "CEN-TUNE-009",
        "categoria": "gobernanza_y_riesgo",
        "instruction": "Describe el protocolo ante pérdida de cadena de frío en fármacos termolábiles.",
        "input": "Incidente: Ruptura térmica en recepción de Insulina Humana NPH.",
        "output": "PROTOCOLO: Rechazo inmediato del 100% del embarque fuera del rango de 2°C a 8°C. El laboratorio dispone de un plazo perentorio de 48 horas para reponer el stock íntegro sin que se suspenda el cómputo de días de atraso ni las multas diarias asociadas."
    },
    {
        "id": "CEN-TUNE-010",
        "categoria": "gobernanza_y_riesgo",
        "instruction": "Determina si un sistema de IA puede autorizar una adjudicación con sobreprecio superior al 15%.",
        "input": "Escenario: Adjudicación propuesta para Insulina NPH a $4.500 CLP (+18.42% de desvío).",
        "output": "POLÍTICA DE CONTROL HUMANO: NEGATIVO. La IA tiene estrictamente prohibida la adjudicación autónoma de compras con sobreprecio superior al 15.0%. El flujo debe pausarse mediante interrupt() y requerir la autorización expresa y formal del Jefe de Adquisiciones de CENABAST."
    }
]


# -----------------------------------------------------------------------------
# 2. Función de Diagnóstico y Validación Sintáctica del Dataset
# -----------------------------------------------------------------------------
def validar_dataset(dataset: List[Dict[str, Any]]) -> Tuple[bool, Dict[str, Any]]:
    """
    Valida la integridad estructural, balance por categoría y ausencia de duplicados.
    
    Verificaciones:
    1. Presencia de campos obligatorios ('instruction', 'input', 'output').
    2. Strings no vacíos en cada campo.
    3. Conteo y balance proporcional por categoría.
    4. Detección de instrucciones duplicadas.
    """
    errores = []
    campos_requeridos = {"id", "categoria", "instruction", "input", "output"}
    instrucciones_vistas = set()
    conteo_categorias = Counter()

    for idx, item in enumerate(dataset):
        # 1. Campos presentes
        faltantes = campos_requeridos - set(item.keys())
        if faltantes:
            errores.append(f"Fila {idx} (ID: {item.get('id', 'desconocido')}): Faltan campos {faltantes}")

        # 2. Contenido no vacío
        for campo in ["instruction", "input", "output"]:
            val = item.get(campo, "")
            if not isinstance(val, str) or not val.strip():
                errores.append(f"Fila {idx}: Campo '{campo}' está vacío o no es string.")

        # 3. Duplicados
        instr = item.get("instruction", "").strip().lower()
        if instr in instrucciones_vistas:
            errores.append(f"Fila {idx}: Instrucción duplicada: '{instr[:40]}...'")
        instrucciones_vistas.add(instr)

        # 4. Conteo de categorías
        cat = item.get("categoria", "sin_categoria")
        conteo_categorias[cat] += 1

    es_valido = len(errores) == 0
    diagnostico = {
        "valido": es_valido,
        "total_ejemplos": len(dataset),
        "distribucion_categorias": dict(conteo_categorias),
        "errores": errores,
    }
    return es_valido, diagnostico


def main():
    print("=" * 70)
    print("  VALIDACIÓN DEL DATASET DE PERSONALIZACIÓN (BLOQUE 29)")
    print("=" * 70)

    valido, diag = validar_dataset(DATASET_CENABAST)
    print(f"Estado de Validación: {'APROBADO (Válido)' if valido else 'RECHAZADO'}")
    print(f"Total ejemplos:       {diag['total_ejemplos']}")
    print("Distribución por Categoría:")
    for cat, conteo in diag["distribucion_categorias"].items():
        print(f"  - {cat}: {conteo} ejemplos")

    if diag["errores"]:
        print("\nErrores detectados:")
        for err in diag["errores"]:
            print(f"  ✗ {err}")
    else:
        print("\n✓ Todos los ejemplos cumplen con los estándares de instrucción/salida para tuning.")


if __name__ == "__main__":
    main()
