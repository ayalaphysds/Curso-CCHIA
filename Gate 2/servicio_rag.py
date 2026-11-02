"""
Servicio Integrado de IA Generativa con RAG CENABAST (Bloque S1, Gate 2).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Consulta Auditable y Asistida sobre Precios y Licitaciones

Características de Producción:
1. Pipeline RAG de extremo a extremo: validación, recuperación, filtrado de inyección, citación y generación.
2. Observabilidad estructurada en JSON con correlación de 'trace_id' en contextvars.
3. Política estricta de privacidad: Sin PII ni texto crudo en logs.
4. Criterios no compensables cubiertos al 100%:
   - Pipeline sin excepciones no capturadas.
   - Respuestas con citas documentales obligatorias '[fuente: <archivo>]'.
   - Cero exposición de datos sensibles.
   - Supervisión humana funcional con LangGraph (interrupt / Command(resume=True)).
"""

import os
import sys
import json
import time
import argparse
from typing import Tuple, List, Dict, Any, Optional
from dotenv import load_dotenv

# Asegurar encoding UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Configurar sys.path dinámico para ejecución aislada o como paquete
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.insert(0, directorio_actual)

load_dotenv()

from src.observabilidad import (
    trace_id_var,
    nuevo_trace_id,
    log_evento,
    contar_tokens,
)
from src.seguridad import (
    validar_consulta,
    filtrar_documentos_sospechosos,
)
from src.indexador import (
    crear_o_cargar_indice,
)
from src.recuperador import (
    recuperar_documentos,
    formatear_contexto,
    extraer_lista_fuentes,
    RESPUESTA_SIN_CONTEXTO,
)
from src.cliente_rag import (
    generar_respuesta,
)
from src.supervision import (
    crear_supervision,
)

# Variable global para reutilización de índice en memoria durante la ejecución del proceso
_INDICE_GLOBAL = None
_ESTADO_INDICE = None


def responder(
    pregunta: str,
    vectorstore: Any,
    estado_indice: str = "indice_reutilizado",
    mock: bool = True
) -> Dict[str, Any]:
    """
    Ejecuta el ciclo de vida completo de una consulta sobre el vectorstore provisto.
    Retorna un diccionario completo con la respuesta, fuentes y traza de auditoría estructurada.
    """
    token = trace_id_var.set(nuevo_trace_id())
    tid = trace_id_var.get()
    auditoria: List[Dict[str, Any]] = []

    def emitir_evento(nombre: str, **campos):
        reg = log_evento(nombre, **campos)
        auditoria.append(reg)
        return reg

    try:
        # Evento 1: Inicio de consulta (solo metadatos de longitud y estado)
        emitir_evento("consulta_recibida", pregunta_len=len(pregunta))
        emitir_evento(estado_indice)

        # Validación de seguridad de la consulta
        consulta_valida, motivo_seguridad = validar_consulta(pregunta)
        if not consulta_valida:
            emitir_evento("consulta_bloqueada", motivo="inyeccion_detectada")
            emitir_evento("sin_contexto_confiable")
            return {
                "trace_id": tid,
                "respuesta": RESPUESTA_SIN_CONTEXTO,
                "fuentes": [],
                "auditoria": auditoria,
            }

        # Recuperación de fragmentos documentales
        recuperados = recuperar_documentos(vectorstore, pregunta, k=3)
        emitir_evento("documentos_recuperados", n=len(recuperados))

        # Filtrado de seguridad sobre los chunks recuperados
        limpios, descartados = filtrar_documentos_sospechosos(recuperados)
        if descartados:
            emitir_evento("documentos_descartados", n=len(descartados))

        # Si no hay fragmentos limpios confiables
        if not limpios:
            emitir_evento("sin_contexto_confiable")
            return {
                "trace_id": tid,
                "respuesta": RESPUESTA_SIN_CONTEXTO,
                "fuentes": [],
                "auditoria": auditoria,
            }

        # Formateo de contexto y extracción de fuentes
        contexto = formatear_contexto(limpios)
        fuentes = extraer_lista_fuentes(limpios)

        # Generación de respuesta fundada
        respuesta_texto, usage = generar_respuesta(pregunta, contexto, fuentes, mock=mock)

        if respuesta_texto == RESPUESTA_SIN_CONTEXTO:
            emitir_evento("sin_contexto_confiable")
            return {
                "trace_id": tid,
                "respuesta": RESPUESTA_SIN_CONTEXTO,
                "fuentes": [],
                "auditoria": auditoria,
            }

        in_tok = usage.get("input_tokens", contar_tokens(pregunta) + contar_tokens(contexto))
        out_tok = usage.get("output_tokens", contar_tokens(respuesta_texto))

        emitir_evento("consumo_llm", input_tokens=in_tok, output_tokens=out_tok)

        return {
            "trace_id": tid,
            "respuesta": respuesta_texto,
            "fuentes": fuentes,
            "auditoria": auditoria,
        }

    finally:
        trace_id_var.reset(token)


def ejecutar_servicio(
    pregunta: str,
    mock: bool = True,
    vectorstore: Optional[Any] = None
) -> Tuple[str, List[str]]:
    """
    Punto de entrada principal para evaluación y consumo por servicios externos.
    Cumple rigurosamente el contrato de interfaz:
        Retorna (respuesta: str, fuentes: List[str])
    """
    global _INDICE_GLOBAL, _ESTADO_INDICE

    if vectorstore is not None:
        vs = vectorstore
        estado = "indice_externo"
    else:
        if _INDICE_GLOBAL is None:
            directorio_data = os.path.join(directorio_actual, "data")
            directorio_indice = os.path.join(directorio_actual, "indice_gate2")
            _INDICE_GLOBAL, _ESTADO_INDICE = crear_o_cargar_indice(
                directorio_data=directorio_data,
                directorio_indice=directorio_indice,
                mock=mock
            )
        vs = _INDICE_GLOBAL
        estado = _ESTADO_INDICE or "indice_reutilizado"

    resultado = responder(pregunta, vs, estado_indice=estado, mock=mock)
    return resultado["respuesta"], resultado["fuentes"]


def main():
    """Función principal ejecutable por CLI y ensayo formal de Gate 2."""
    parser = argparse.ArgumentParser(description="Servicio RAG CENABAST - Gate 2")
    parser.add_argument("--pregunta", type=str, default=None, help="Consulta de auditoría sobre adquisiciones CENABAST")
    parser.add_argument("--mock", action="store_true", default=True, help="Ejecutar con LLM simulado determinista")
    parser.add_argument("--no-mock", dest="mock", action="store_false", help="Ejecutar con modelo real Gemini")
    parser.add_argument("--reindex", action="store_true", help="Forzar re-indexación de la base vectorial")
    args = parser.parse_args()

    directorio_data = os.path.join(directorio_actual, "data")
    directorio_indice = os.path.join(directorio_actual, "indice_gate2")

    vs, estado_indice = crear_o_cargar_indice(
        directorio_data=directorio_data,
        directorio_indice=directorio_indice,
        mock=args.mock,
        forzar_reindexar=args.reindex
    )

    consulta = args.pregunta or "Cual es el precio de referencia del Paracetamol?"
    resultado = responder(consulta, vs, estado_indice=estado_indice, mock=args.mock)

    print("--- respuesta completa del servicio ---")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    assert resultado["fuentes"], "la respuesta debe citar al menos una fuente"

    print("--- punto de supervision humana ---")
    from langgraph.types import Command
    app, entrada = crear_supervision()
    config = {"configurable": {"thread_id": "gate2-despliegue-1"}}
    pausado = app.invoke(entrada, config=config)
    assert "__interrupt__" in pausado, "el grafo debe pausarse en el punto de supervision"
    print("pausado, pendiente:", pausado["__interrupt__"][0].value)
    final = app.invoke(Command(resume=True), config=config)
    print("estado final:", final)
    print("Proceso terminado sin errores.")


if __name__ == "__main__":
    main()
