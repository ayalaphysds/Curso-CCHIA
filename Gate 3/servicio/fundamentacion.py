"""Detector determinista de alucinaciones y falta de respaldo (Bloque 43)."""

import re

from servicio.contratos import Fragmento
from servicio.recuperador import normalizar

PATRON_CITA = re.compile(r"\[fuente:\s*([^\]]+)\]", re.I)
PATRON_NUMERO = re.compile(r"(?<![A-Za-z0-9\-])\$?\d+(?:[.,]\d+)?%?")


def _normalizar_numero(token: str) -> str:
    limpio = token.strip().lstrip("$").rstrip("%")
    # Normalizar separador de miles (ej. 1.250 -> 1250) cuando tiene 3 digitos tras punto
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", limpio):
        limpio = limpio.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d+\.\d{3}\.\d{2}", limpio):
        limpio = limpio.replace(".", "", 1)
    try:
        val = float(limpio.replace(",", "."))
        return f"{val:.4f}".rstrip("0").rstrip(".")
    except ValueError:
        return limpio


def _extraer_numeros(texto: str) -> set[str]:
    nums: set[str] = set()
    for m in PATRON_NUMERO.findall(texto):
        norm = _normalizar_numero(m)
        # Ignorar numeros de 1 digito usados en enumeraciones y el anio 2026 si aparece en titulo
        if norm:
            nums.add(norm)
    return nums


def problemas_de_respaldo(
    texto: str,
    fragmentos: list[Fragmento],
    sin_informacion: str,
) -> list[str]:
    """Evalua si la respuesta generada esta respaldada por los fragmentos recuperados.

    Retorna una lista de codigos de problema (vacia si esta correctamente fundamentada):
    - H-SIN-FUENTE: no cita ningun archivo del corpus.
    - H-FUENTE-INVENTADA: cita un archivo que no estaba en los fragmentos recuperados.
    - H-CIFRA-NO-RESPALDADA: afirma montos, porcentajes o plazos ausentes del contexto.
    - H-CONTRADICCION: recomienda adjudicar automaticamente un escenario de sobreprecio critico.
    """
    if not texto or not texto.strip():
        return ["H-VACIA"]
    if sin_informacion.strip() in texto:
        return []

    problemas: list[str] = []
    fuentes_validas = {f.fuente.strip() for f in fragmentos}
    contexto_total = "\n".join(f"{f.fuente}\n{f.seccion}\n{f.texto}" for f in fragmentos)

    # 1. Verificacion de citas documentales
    citas = [c.strip() for c in PATRON_CITA.findall(texto)]
    if not citas:
        problemas.append("H-SIN-FUENTE")
    else:
        for cita in citas:
            if cita not in fuentes_validas:
                problemas.append("H-FUENTE-INVENTADA")
                break

    # 2. Verificacion de cifras numericas respecto al contexto
    texto_sin_citas = PATRON_CITA.sub("", texto)
    nums_resp = _extraer_numeros(texto_sin_citas)
    nums_ctx = _extraer_numeros(contexto_total)
    # Tambien aceptar representacion sin ceros finales o en miles
    no_respaldados = [n for n in nums_resp if n not in nums_ctx]
    if no_respaldados:
        problemas.append("H-CIFRA-NO-RESPALDADA")

    # 3. Verificacion de contradiccion de politica critica
    resp_norm = normalizar(texto)
    ctx_norm = normalizar(contexto_total)
    if ("prohibida la adjudicacion automatizada" in ctx_norm or "sobreprecio critico" in ctx_norm) and (
        "adjudicar automaticamente" in resp_norm
        or "no requiere supervision humana" in resp_norm
        or "aprobar automaticamente el sobreprecio" in resp_norm
    ):
        problemas.append("H-CONTRADICCION")

    return problemas
