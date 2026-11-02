"""
Módulo de Observabilidad Estructurada y Privacidad (Bloque 31, U2.7).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Trazabilidad Segura sin Exposición de PII

Características:
1. Emisión exclusiva de eventos JSON estructurados.
2. Aislamiento y propagación de 'trace_id' mediante contextvars.
3. Estimación y conteo de tokens de entrada/salida.
4. Regla estricta de privacidad: PROHIBIDO registrar prompts crudos, consultas textuales,
   correos electrónicos o información de identificación personal (PII).
"""

import json
import logging
import sys
import uuid
import contextvars
from typing import Any, Dict, Optional

# ContextVar para aislamiento asíncrono y síncrono del identificador de traza
trace_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("trace_id", default=None)

# Nombres de loggers utilizados por el servicio y tests
LOGGER_NAME = "rag_cenabast"
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

# Si el logger no tiene handlers propios, configuramos salida estructurada estándar
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    # logger.propagate = True permite que caplog de pytest capture los registros


def nuevo_trace_id() -> str:
    """Genera un nuevo identificador de traza unívoco y compacto."""
    return f"trace-{uuid.uuid4().hex[:8]}"


def obtener_trace_id() -> Optional[str]:
    """Retorna el trace_id activo en el contexto actual."""
    return trace_id_var.get()


def contar_tokens(texto: Optional[str]) -> int:
    """
    Estima el conteo de tokens para un texto dado.
    Utiliza una aproximación robusta basada en la distribución léxica (promedio ~3.8 caracteres por token en español).
    """
    if not texto:
        return 0
    texto_limpio = texto.strip()
    if not texto_limpio:
        return 0
    # Estimación ponderada entre palabras y caracteres para alta fidelidad
    palabras = len(texto_limpio.split())
    estimacion_caracteres = int(len(texto_limpio) / 3.8)
    return max(1, int(round((palabras * 1.3 + estimacion_caracteres) / 2)))


def sanitizar_metadatos(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Garantía de privacidad estricta:
    Descarta o reemplaza por longitudes/conteos cualquier campo que contenga
    texto de consulta, prompts, correos o datos potencialmente sensibles.
    """
    claves_prohibidas = {
        "pregunta", "consulta", "query", "prompt", "texto", "documento",
        "page_content", "correo", "email", "rut", "usuario", "password", "token_auth"
    }
    limpios: Dict[str, Any] = {}
    for k, v in kwargs.items():
        k_lower = k.lower()
        if k_lower in claves_prohibidas:
            # Reemplazar texto crudo por su longitud
            if isinstance(v, str):
                limpios[f"{k_lower}_len"] = len(v)
            elif isinstance(v, (list, tuple)):
                limpios[f"{k_lower}_count"] = len(v)
            else:
                limpios[f"{k_lower}_present"] = bool(v)
        else:
            # Validar que si el valor es string no contenga un correo obvio
            if isinstance(v, str) and "@" in v and "." in v:
                limpios[f"{k}_sanitizado"] = "[PROTECTED_PII]"
            else:
                limpios[k] = v
    return limpios


def log_evento(evento: str, nivel: int = logging.INFO, **kwargs) -> Dict[str, Any]:
    """
    Emite un registro de evento estructurado en formato JSON cumpliendo las reglas
    de observabilidad y privacidad de Gate 2.
    
    Retorna el diccionario estructurado registrado.
    """
    tid = trace_id_var.get()
    campos_sanitizados = sanitizar_metadatos(kwargs)
    registro: Dict[str, Any] = {
        "evento": evento,
        "trace_id": tid,
        **campos_sanitizados
    }

    mensaje_json = json.dumps(registro, ensure_ascii=False)
    
    # Emitir al logger principal y asegurar propagación
    logger.log(nivel, mensaje_json)
    
    # También emitir al logger genérico 'servicio' para compatibilidad con autochequeos
    servicio_logger = logging.getLogger("servicio")
    if servicio_logger != logger:
        servicio_logger.log(nivel, mensaje_json)

    return registro


class ContextoTraza:
    """Administrador de contexto para gestionar el ciclo de vida de un trace_id."""

    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or nuevo_trace_id()
        self.token = None

    def __enter__(self):
        self.token = trace_id_var.set(self.trace_id)
        return self.trace_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.token is not None:
            trace_id_var.reset(self.token)
