"""Contratos de datos entre componentes internos de la cadena CENABAST (Bloque 39)."""

from dataclasses import dataclass
from typing import Any


class ContratoInvalido(ValueError):
    """Se lanza cuando un componente rompe el contrato de interfaz esperado."""


@dataclass(frozen=True)
class Fragmento:
    fuente: str
    seccion: str
    texto: str
    puntaje: float


def verificar_fragmento(fragmento: Any) -> Fragmento:
    if not isinstance(fragmento, Fragmento):
        raise ContratoInvalido(f"Se esperaba Fragmento, se recibio {type(fragmento).__name__}")
    if not fragmento.fuente.strip():
        raise ContratoInvalido("Fragmento sin campo 'fuente' no vacio")
    if not fragmento.texto.strip():
        raise ContratoInvalido("Fragmento sin campo 'texto' no vacio")
    if fragmento.puntaje < 0:
        raise ContratoInvalido(f"Puntaje negativo invalido: {fragmento.puntaje}")
    return fragmento


def empaquetar_respuesta(
    respuesta: str,
    fuentes: list[str],
    trace_id: str,
    modo_modelo: str,
    advertencia_respaldo: str | None = None,
) -> dict[str, Any]:
    if not isinstance(respuesta, str) or not respuesta.strip():
        raise ContratoInvalido("La respuesta empaquetada debe ser un texto no vacio")
    if not isinstance(fuentes, list) or not all(isinstance(f, str) and f.strip() for f in fuentes):
        raise ContratoInvalido("Las fuentes deben ser una lista de nombres de archivo no vacios")
    if not isinstance(trace_id, str) or not trace_id.strip():
        raise ContratoInvalido("trace_id obligatorio en la respuesta empaquetada")
    if modo_modelo not in ("simulado", "real", "respaldo"):
        raise ContratoInvalido(f"modo_modelo invalido: {modo_modelo}")

    # Deduplicar fuentes preservando orden
    fuentes_unicas = list(dict.fromkeys(fuentes))
    return {
        "respuesta": respuesta.strip(),
        "fuentes": fuentes_unicas,
        "trace_id": trace_id,
        "modo_modelo": modo_modelo,
        "advertencia_respaldo": advertencia_respaldo,
    }
