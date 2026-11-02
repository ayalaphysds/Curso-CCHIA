"""
Pipeline de procesamiento de texto y cálculo de métricas léxicas (Bloque 15 y 16, U2.2).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría de Adquisiciones Hospitalarias

Funciones principales:
1. procesar_texto(texto): Normalización a minúsculas, remoción de signos de puntuación mediante regex
   y tokenización limpia. Maneja robustamente textos vacíos y cadenas compuestas solo por puntuación.
2. calcular_metricas(referencia, respuesta): Cálculo exacto de Precisión, Cobertura (Recall) y F1-Score
   utilizando collections.Counter para evaluar coincidencia léxica sobre respuestas generadas vs referencias.
"""

import re
from collections import Counter
from typing import List, Dict


def procesar_texto(texto: str) -> List[str]:
    """
    Normaliza y tokeniza un texto en español.
    
    Pasos:
    1. Validación de tipo: Si no es string o está vacío, retorna lista vacía [].
    2. Conversión a minúsculas.
    3. Remoción de caracteres no alfanuméricos y puntuación preservando acentos/tildes y números.
    4. Segmentación en tokens mediante split().
    
    Retorna:
        List[str]: Lista ordenada de tokens limpios. Si la entrada contenía solo signos
                   de puntuación o espacios, retorna [].
    """
    if not isinstance(texto, str) or not texto.strip():
        return []

    # 1. Minúsculas
    texto_min = texto.lower()

    # 2. Reemplazo de puntuación y guión bajo por espacios
    # [^\w\s]|_ elimina signos ortográficos y underscores
    texto_limpio = re.sub(r"[^\w\s]|_", " ", texto_min)

    # 3. Tokenización por espacios en blanco múltiples
    tokens = [t for t in texto_limpio.split() if t]
    return tokens


def calcular_metricas(referencia: str, respuesta: str) -> Dict[str, float]:
    """
    Calcula Precisión, Cobertura (Recall) y F1-Score léxico a nivel de tokens usando Counter.
    
    Parámetros:
        referencia: Texto modelo o ground-truth esperado.
        respuesta: Texto generado por el modelo o sistema.
        
    Retorna:
        Dict con claves:
        - "precision": tokens_coincidentes / tokens_respuesta (0.0 si respuesta vacía)
        - "cobertura": tokens_coincidentes / tokens_referencia (0.0 si referencia vacía)
        - "f1": media armónica entre precisión y cobertura
    """
    tokens_ref = procesar_texto(referencia)
    tokens_resp = procesar_texto(respuesta)

    if not tokens_resp or not tokens_ref:
        return {
            "precision": 0.0,
            "cobertura": 0.0,
            "f1": 0.0,
            "tokens_referencia": len(tokens_ref),
            "tokens_respuesta": len(tokens_resp),
            "tokens_comunes": 0,
        }

    c_ref = Counter(tokens_ref)
    c_resp = Counter(tokens_resp)

    # Intersección multiconjunto: cuenta el mínimo de repeticiones de cada palabra
    interseccion = c_ref & c_resp
    tokens_comunes = sum(interseccion.values())

    precision = tokens_comunes / len(tokens_resp) if len(tokens_resp) > 0 else 0.0
    cobertura = tokens_comunes / len(tokens_ref) if len(tokens_ref) > 0 else 0.0

    if precision + cobertura > 0:
        f1 = 2 * (precision * cobertura) / (precision + cobertura)
    else:
        f1 = 0.0

    return {
        "precision": round(precision, 4),
        "cobertura": round(cobertura, 4),
        "f1": round(f1, 4),
        "tokens_referencia": len(tokens_ref),
        "tokens_respuesta": len(tokens_resp),
        "tokens_comunes": tokens_comunes,
    }


if __name__ == "__main__":
    demo_ref = "El precio de referencia para Paracetamol 500 mg es de 22.40 pesos chilenos."
    demo_resp = "Paracetamol 500 mg tiene un precio de referencia de 22.40 CLP."
    metricas = calcular_metricas(demo_ref, demo_resp)
    print("Demostración de Métricas Léxicas (Bloque 15-16):")
    print(f"Referencia: {demo_ref}")
    print(f"Respuesta:  {demo_resp}")
    print(f"Resultado:  {metricas}")
