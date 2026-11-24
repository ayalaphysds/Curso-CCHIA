"""Plantilla versionada de prompts con huella SHA-256 (Bloque 39 y 43)."""

import hashlib

from servicio.contratos import Fragmento

VERSION_PROMPT = "v3.0-cenabast-capstone"

INSTRUCCION = (
    "Eres el asistente oficial de auditoria de precios y licitaciones de CENABAST. "
    "Responde exclusivamente usando los fragmentos del contexto institucional provisto. "
    "Cita siempre el archivo exacto con el formato [fuente: <archivo>]. "
    "Si el contexto no contiene la respuesta, responde exactamente: "
    "'No encuentro esa informacion en la documentacion oficial de CENABAST.'"
)

HUELLA_PROMPT = hashlib.sha256(INSTRUCCION.encode("utf-8")).hexdigest()[:12]


def construir_prompt(pregunta: str, fragmentos: list[Fragmento]) -> str:
    if not pregunta or not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacia para construir el prompt")
    if not fragmentos:
        raise ValueError("Se requiere al menos un fragmento de contexto")

    bloques = []
    for idx, frag in enumerate(fragmentos, 1):
        bloques.append(f"[{idx}] ({frag.fuente} | {frag.seccion})\n{frag.texto}")

    contexto = "\n\n".join(bloques)
    return (
        f"INSTRUCCION ({VERSION_PROMPT} | {HUELLA_PROMPT}):\n{INSTRUCCION}\n\n"
        f"CONTEXTO OFICIAL CENABAST:\n{contexto}\n\n"
        f"PREGUNTA DEL ANALISTA:\n{pregunta.strip()}\n"
    )
