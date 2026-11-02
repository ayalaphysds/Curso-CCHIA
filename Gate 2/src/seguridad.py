"""
Módulo de Seguridad y Mitigación de Inyección de Prompts (Bloque 31, U2.7).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Protección Integral contra Inyección en RAG

Características:
1. Filtro riguroso de patrones de inyección y manipulación de instrucciones.
2. Análisis bidireccional: valida tanto la consulta del usuario como los fragmentos (Document.page_content) recuperados.
3. Descarte preventivo de chunks contaminados antes del ensamblaje del prompt.
4. Registro de eventos de seguridad auditable sin filtrar el contenido hostil completo.
"""

import re
from typing import List, Tuple, Optional
from langchain_core.documents import Document

# Patrones canónicos de inyección y manipulación detectados en benchmarks de seguridad
PATRONES_INYECCION = [
    # Inyecciones en español (con o sin 'anteriores'/'previas', directas)
    r"ignora(?:r)?\s+(?:todas\s+)?(?:las\s+)?(?:siguientes\s+)?(?:instrucciones|reglas|directrices)\b",
    r"olvida(?:r)?\s+(?:todas\s+)?(?:las\s+)?(?:reglas|instrucciones|directrices)\b",
    r"nuevo\s+sistema\s*:",
    r"revela(?:r)?\s+(?:tu|el)?\s*(?:system\s+)?prompt\b",
    r"act[uú]a\s+como\s+administrador\s+del\s+sistema",
    r"adjudica(?:r)?\s+directamente\b",
    r"\badjudica(?:r|ción)?\s+directa\b",
    r"eval[uú]a\s+como\s+adjudicar",

    # Inyecciones en inglés (incluyendo sinónimos: guidelines, dump, leak)
    r"ignore\s+(?:all\s+)?(?:previous\s+)?(?:instructions|guidelines|rules|prompts)\b",
    r"(?:reveal|dump|print|display|leak|show|output)\s+(?:all\s+)?(?:your\s+)?(?:the\s+)?(?:system\s+)?prompt\b",
    r"new\s+system\s*:",

    # Delimitadores y overrides
    r"(?:instruction|system|prompt)\s*override\b",
    r"override\s+(?:instruction|system|prompt|rules)\b",
    r"system\s*:\s*override",
    r"bypass\s+governance\b",
    r"jailbreak\b",
    r"dan\s+mode\b",
    r"drop\s+table\b",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in PATRONES_INYECCION]


def detectar_inyeccion(texto: Optional[str]) -> List[str]:
    """
    Inspecciona una cadena de texto en busca de patrones maliciosos conocidos.
    Retorna la lista de patrones detectados (vacía si el texto es seguro).
    """
    if not texto or not isinstance(texto, str):
        return []

    coincidencias = []
    for pattern in COMPILED_PATTERNS:
        match = pattern.search(texto)
        if match:
            coincidencias.append(pattern.pattern)
    return coincidencias


def es_contenido_seguro(texto: Optional[str]) -> Tuple[bool, str]:
    """
    Determina si un texto dado cumple con las directivas de seguridad.
    Retorna: (es_seguro: bool, motivo: str).
    """
    if not texto or not isinstance(texto, str):
        return True, "Texto vacío o nulo"

    coincidencias = detectar_inyeccion(texto)
    if coincidencias:
        return False, f"Patrón sospechoso detectado: {coincidencias[0]}"
    return True, "Contenido validado"


def filtrar_documentos_sospechosos(documentos: List[Document]) -> Tuple[List[Document], List[Document]]:
    """
    Filtra una colección de objetos Document de LangChain evaluando 'd.page_content'.
    
    Retorna:
        Tuple:
        - limpios (List[Document]): Documentos validados y libres de amenazas.
        - descartados (List[Document]): Documentos que contienen patrones de inyección.
    """
    limpios: List[Document] = []
    descartados: List[Document] = []

    for doc in documentos:
        contenido = getattr(doc, "page_content", "")
        coincidencias = detectar_inyeccion(contenido)
        if coincidencias:
            descartados.append(doc)
        else:
            limpios.append(doc)

    return limpios, descartados


def validar_consulta(consulta: Optional[str]) -> Tuple[bool, str]:
    """
    Valida la consulta de entrada antes de iniciar el pipeline RAG.
    """
    if not consulta or not str(consulta).strip():
        return False, "Consulta vacía o sin contenido legible"

    coincidencias = detectar_inyeccion(consulta)
    if coincidencias:
        return False, f"Inyección de prompt detectada en la consulta: {coincidencias[0]}"

    return True, "Consulta autorizada"
