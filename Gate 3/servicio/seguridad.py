"""Seguridad, defensa contra inyeccion de prompts y logging estructurado sin PII (Bloque 43)."""

import contextvars
import json
import logging
import re
import uuid
from typing import Any

trace_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)

logger = logging.getLogger("servicio")
logger.setLevel(logging.INFO)

MENSAJE_BLOQUEO = "No puedo atender esa solicitud por razones de seguridad."

PATRONES_INYECCION = [
    re.compile(r"ignora(?:r)?\s+(?:todas\s+)?(?:las\s+)?(?:siguientes\s+|anteriores\s+|previas\s+)?(?:instrucciones|reglas|directrices)\b", re.I),
    re.compile(r"olvida(?:r)?\s+(?:todas\s+)?(?:las\s+)?(?:reglas|instrucciones|directrices)\b", re.I),
    re.compile(r"revela(?:r)?\s+(?:tu|el)?\s*(?:system\s+)?prompt\b", re.I),
    re.compile(r"mu[eé]stra(?:me)?\s+(?:tu|tus|la|las|el|los)\s+(?:instrucciones\s+internas|claves?|api\s*key|secretos?|credenciales)\b", re.I),
    re.compile(r"act[uú]a\s+como\s+(?:administrador|root|sistema|otro\s+asistente)\b", re.I),
    re.compile(r"adjudica(?:r)?\s+directamente\b", re.I),
    re.compile(r"nuevo\s+sistema\s*:", re.I),
    re.compile(r"ignore\s+(?:all\s+)?(?:previous\s+)?(?:instructions|guidelines|rules|prompts)\b", re.I),
    re.compile(r"(?:reveal|dump|print|leak|show)\s+(?:all\s+)?(?:your\s+)?(?:the\s+)?(?:system\s+)?prompt\b", re.I),
    re.compile(r"(?:instruction|system|prompt)\s*override\b|override\s+(?:instructions|system|rules)\b", re.I),
    re.compile(r"\bjailbreak\b|\bdan\s+mode\b|\bbypass\s+governance\b", re.I),
    re.compile(r"dime\s+un\s+chiste\b|cu[eé]ntame\s+un\s+chiste\b", re.I),
]

PATRON_CLAVE_GOOGLE = re.compile(r"AIza[0-9A-Za-z_\-]{20,}")
PATRON_EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
PATRON_RUT = re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")

CLAVES_SENSIBLES = {
    "pregunta",
    "consulta",
    "query",
    "prompt",
    "texto",
    "respuesta",
    "correo",
    "email",
    "rut",
    "api_key",
    "clave",
    "secret",
    "token",
}


def nuevo_trace_id() -> str:
    return f"trace-{uuid.uuid4().hex[:8]}"


def detectar_inyeccion(texto: str) -> list[str]:
    if not texto or not isinstance(texto, str):
        return []
    return [p.pattern for p in PATRONES_INYECCION if p.search(texto)]


def es_consulta_segura(texto: str) -> tuple[bool, str]:
    coincidencias = detectar_inyeccion(texto)
    if coincidencias:
        return False, "inyeccion_detectada"
    return True, "ok"


def filtrar_fragmentos(fragmentos: list[Any]) -> tuple[list[Any], int]:
    limpios = []
    descartados = 0
    for frag in fragmentos:
        if detectar_inyeccion(getattr(frag, "texto", "")):
            descartados += 1
        else:
            limpios.append(frag)
    return limpios, descartados


def limpiar_salida(texto: str, internos: list[str] | None = None) -> str:
    resultado = texto
    for bloque in internos or []:
        if bloque and bloque in resultado:
            resultado = resultado.replace(bloque, "")
    resultado = PATRON_CLAVE_GOOGLE.sub("[CLAVE_REDACTADA]", resultado)
    resultado = PATRON_EMAIL.sub("[PII_REDACTADO]", resultado)
    resultado = PATRON_RUT.sub("[RUT_REDACTADO]", resultado)
    return re.sub(r"\s{2,}", " ", resultado).strip()


def log_evento(evento: str, nivel: int = logging.INFO, **campos: Any) -> dict[str, Any]:
    seguros: dict[str, Any] = {}
    for k, v in campos.items():
        if k.lower() in CLAVES_SENSIBLES:
            if isinstance(v, str):
                seguros[f"{k}_len"] = len(v)
            else:
                seguros[f"{k}_omitido"] = True
        elif isinstance(v, str) and (
            PATRON_CLAVE_GOOGLE.search(v) or PATRON_EMAIL.search(v) or PATRON_RUT.search(v)
        ):
            seguros[k] = "[REDACTADO]"
        else:
            seguros[k] = v

    registro = {"evento": evento, "trace_id": trace_id_var.get(), **seguros}
    logger.log(nivel, json.dumps(registro, ensure_ascii=False))
    return registro
