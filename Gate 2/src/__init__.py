"""
Paquete modular de componentes de IA para Gate 2 - CENABAST.
Especialización en IA Accenture - Curso CCHIA
"""

from src.observabilidad import (
    trace_id_var,
    nuevo_trace_id,
    obtener_trace_id,
    contar_tokens,
    log_evento,
    ContextoTraza,
)
from src.seguridad import (
    detectar_inyeccion,
    es_contenido_seguro,
    filtrar_documentos_sospechosos,
    validar_consulta,
)
from src.indexador import (
    crear_o_cargar_indice,
    cargar_documentos_desde_directorio,
    segmentar_documentos,
    obtener_embeddings,
)
from src.recuperador import (
    recuperar_documentos,
    recuperar_y_procesar,
    formatear_contexto,
    extraer_lista_fuentes,
    armar_prompt_rag,
    RESPUESTA_SIN_CONTEXTO,
)
from src.cliente_rag import (
    generar_respuesta,
    generar_respuesta_mock,
)
from src.supervision import (
    crear_supervision,
    crear_grafo_supervision_precios,
)
from src.evaluador import (
    calcular_metricas_recuperacion,
    verificar_citas_en_respuesta,
    calcular_costo_y_latencia,
)

__all__ = [
    "trace_id_var",
    "nuevo_trace_id",
    "obtener_trace_id",
    "contar_tokens",
    "log_evento",
    "ContextoTraza",
    "detectar_inyeccion",
    "es_contenido_seguro",
    "filtrar_documentos_sospechosos",
    "validar_consulta",
    "crear_o_cargar_indice",
    "cargar_documentos_desde_directorio",
    "segmentar_documentos",
    "obtener_embeddings",
    "recuperar_documentos",
    "recuperar_y_procesar",
    "formatear_contexto",
    "extraer_lista_fuentes",
    "armar_prompt_rag",
    "RESPUESTA_SIN_CONTEXTO",
    "generar_respuesta",
    "generar_respuesta_mock",
    "crear_supervision",
    "crear_grafo_supervision_precios",
    "calcular_metricas_recuperacion",
    "verificar_citas_en_respuesta",
    "calcular_costo_y_latencia",
]
