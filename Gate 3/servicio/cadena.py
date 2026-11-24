"""Orquestacion de la cadena RAG de 4 capas con observabilidad y contencion (Gate 3)."""

import logging

from servicio import fundamentacion, prompt as mod_prompt, recuperador, respaldo, seguridad
from servicio.contratos import empaquetar_respuesta

logger = logging.getLogger("servicio.cadena")

SIN_INFORMACION = "No encuentro esa informacion en la documentacion oficial de CENABAST."


def ejecutar(pregunta: str, k: int = 3) -> dict:
    """Ejecuta el flujo completo de 4 capas:
    1. Filtro de seguridad sobre la consulta.
    2. Recuperacion documental + filtro de fragmentos.
    3. Prompt versionado + seleccion de modelo (con respaldo declarado o 503).
    4. Limpieza de salida + verificacion de fundamentacion contra alucinaciones.
    """
    tid = seguridad.nuevo_trace_id()
    token = seguridad.trace_id_var.set(tid)
    try:
        seguridad.log_evento("consulta_recibida", pregunta_len=len(pregunta))

        # Capa 1: seguridad de entrada
        segura, motivo = seguridad.es_consulta_segura(pregunta)
        if not segura:
            seguridad.log_evento("consulta_bloqueada", motivo=motivo)
            return empaquetar_respuesta(
                respuesta=seguridad.MENSAJE_BLOQUEO,
                fuentes=[],
                trace_id=tid,
                modo_modelo="simulado",
                advertencia_respaldo=None,
            )

        # Seleccion de modelo ANTES de abstener para que MODELO=real sin clave falle honestamente (503)
        modelo, modo_modelo, advertencia = respaldo.elegir_modelo()

        # Capa 2: recuperacion y filtrado de fragmentos
        fragmentos_crudos = recuperador.recuperar(pregunta, k=k)
        fragmentos, descartados = seguridad.filtrar_fragmentos(fragmentos_crudos)
        seguridad.log_evento(
            "recuperacion_completada",
            recuperados=len(fragmentos),
            descartados=descartados,
        )

        if not fragmentos:
            seguridad.log_evento("sin_contexto_confiable")
            return empaquetar_respuesta(
                respuesta=SIN_INFORMACION,
                fuentes=[],
                trace_id=tid,
                modo_modelo=modo_modelo,
                advertencia_respaldo=advertencia,
            )

        # Capa 3: construccion de prompt y generacion
        prompt_texto = mod_prompt.construir_prompt(pregunta, fragmentos)
        try:
            texto_bruto = modelo.generar(prompt_texto, pregunta=pregunta, fragmentos=fragmentos)
        except TypeError:
            # Compatibilidad con dobles de prueba de 1 argumento: generar(prompt)
            texto_bruto = modelo.generar(prompt_texto)

        # Capa 4: limpieza de salida y verificacion de fundamentacion
        texto_limpio = seguridad.limpiar_salida(texto_bruto, internos=[mod_prompt.INSTRUCCION])
        problemas = fundamentacion.problemas_de_respaldo(texto_limpio, fragmentos, SIN_INFORMACION)
        if problemas:
            logger.warning("respuesta sin respaldo codigos=%s", ",".join(problemas))
            seguridad.log_evento("alucinacion_contenida", codigos=",".join(problemas))
            return empaquetar_respuesta(
                respuesta=SIN_INFORMACION,
                fuentes=[],
                trace_id=tid,
                modo_modelo=modo_modelo,
                advertencia_respaldo=advertencia,
            )

        fuentes = list(dict.fromkeys(f.fuente for f in fragmentos))
        if SIN_INFORMACION in texto_limpio:
            fuentes = []

        seguridad.log_evento(
            "consulta_respondida",
            n_fuentes=len(fuentes),
            modo_modelo=modo_modelo,
        )
        return empaquetar_respuesta(
            respuesta=texto_limpio,
            fuentes=fuentes,
            trace_id=tid,
            modo_modelo=modo_modelo,
            advertencia_respaldo=advertencia,
        )
    finally:
        seguridad.trace_id_var.reset(token)
