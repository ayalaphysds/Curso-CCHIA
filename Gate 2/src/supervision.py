"""
Módulo de Supervisión Humana con LangGraph (Bloque 32, U2.7).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Control Humano en Adjudicaciones Críticas y Despliegue de Prompts

Cumplimiento Normativo (Criterio No Compensable 4 de Gate 2):
1. Punto de interrupción real interactivo 'interrupt()' que pausa el flujo.
2. Checkpointer 'InMemorySaver' para persistencia transaccional durante la pausa.
3. Reanudación controlada mediante 'Command(resume=True)' que confirma 'aprobado=True'.
"""

from typing import TypedDict, Optional, Dict, Any, Tuple
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class EstadoSupervision(TypedDict):
    """Estado compartido para supervisión humana de despliegues y control de riesgos."""
    huella_nueva: str
    aprobado: bool
    motivo: Optional[str]


def nodo_supervisar_despliegue(estado: EstadoSupervision) -> Dict[str, Any]:
    """
    Nodo de interrupción humana:
    Ejecuta 'interrupt()' para suspender el flujo en el checkpointer.
    Al reanudarse con Command(resume=True/False), adopta el dictamen humano.
    """
    datos_interrupcion = {
        "motivo": "Aprobar despliegue de prompt o adjudicación con sobreprecio en producción",
        "huella_propuesta": estado.get("huella_nueva", "sha256-default"),
    }
    decision = interrupt(datos_interrupcion)
    return {"aprobado": bool(decision is True)}


def nodo_aplicar_decision(estado: EstadoSupervision) -> Dict[str, Any]:
    """Nodo final que ratifica la aplicación de la decisión en el sistema."""
    return {
        "motivo": "Decisión de supervisión aplicada exitosamente" if estado.get("aprobado") else "Rechazado por supervisión humana"
    }


def crear_supervision() -> Tuple[Any, Dict[str, Any]]:
    """
    Función de compatibilidad oficial requerida por la Rúbrica de Gate 2
    y 'test_4_supervision_pausa_y_reanuda'.
    
    Retorna:
        Tuple:
        - app: Grafo StateGraph compilado con InMemorySaver.
        - entrada: Estado inicial dict {'huella_nueva': ..., 'aprobado': False}.
    """
    grafo = StateGraph(EstadoSupervision)
    grafo.add_node("supervisar", nodo_supervisar_despliegue)
    grafo.add_node("aplicar", nodo_aplicar_decision)

    grafo.add_edge(START, "supervisar")
    grafo.add_edge("supervisar", "aplicar")
    grafo.add_edge("aplicar", END)

    app = grafo.compile(checkpointer=InMemorySaver())
    entrada: EstadoSupervision = {
        "huella_nueva": "cenabast-prompt-v2-sha256",
        "aprobado": False,
        "motivo": None
    }
    return app, entrada


# -----------------------------------------------------------------------------
# Grafo Especializado de Supervisión de Precios CENABAST (> 20% Sobreprecio)
# -----------------------------------------------------------------------------
class EstadoAuditoriaPrecio(TypedDict):
    medicamento: str
    precio_ofertado: float
    precio_referencia: float
    desviacion_pct: float
    requiere_supervision: bool
    aprobado: Optional[bool]
    dictamen: str


def nodo_evaluar_desviacion(estado: EstadoAuditoriaPrecio) -> Dict[str, Any]:
    ref = estado.get("precio_referencia", 0.0)
    ofertado = estado.get("precio_ofertado", 0.0)
    desv = ((ofertado - ref) / ref) * 100.0 if ref > 0 else 0.0
    desv_redondeada = round(desv, 2)
    requiere = desv_redondeada > 20.0
    return {
        "desviacion_pct": desv_redondeada,
        "requiere_supervision": requiere,
    }


def enrutar_precio(estado: EstadoAuditoriaPrecio) -> str:
    if estado.get("requiere_supervision", False):
        return "supervisar_sobreprecio"
    return "adjudicar_automatico"


def nodo_supervisar_sobreprecio(estado: EstadoAuditoriaPrecio) -> Dict[str, Any]:
    decision = interrupt({
        "alerta": "SOBREPRECIO_CRITICO_CENABAST",
        "medicamento": estado.get("medicamento"),
        "desviacion_pct": estado.get("desviacion_pct"),
        "mensaje": "Desviación superior al 20%. Requiere autorización expresa de Jefatura de Adquisiciones."
    })
    aprobado = bool(decision is True)
    dictamen = (
        f"Adjudicación autorizada por excepción humana (+{estado.get('desviacion_pct')}%)"
        if aprobado else
        f"Adjudicación RECHAZADA por sobreprecio excesivo (+{estado.get('desviacion_pct')}%)"
    )
    return {"aprobado": aprobado, "dictamen": dictamen}


def nodo_adjudicar_automatico(estado: EstadoAuditoriaPrecio) -> Dict[str, Any]:
    return {
        "aprobado": True,
        "dictamen": f"Adjudicación estándar aprobada (desviación dentro de rango: {estado.get('desviacion_pct')}%)"
    }


def crear_grafo_supervision_precios():
    """Compila el grafo de supervisión para sobreprecios de medicamentos CENABAST."""
    g = StateGraph(EstadoAuditoriaPrecio)
    g.add_node("evaluar", nodo_evaluar_desviacion)
    g.add_node("supervisar_sobreprecio", nodo_supervisar_sobreprecio)
    g.add_node("adjudicar_automatico", nodo_adjudicar_automatico)

    g.add_edge(START, "evaluar")
    g.add_conditional_edges("evaluar", enrutar_precio, {
        "supervisar_sobreprecio": "supervisar_sobreprecio",
        "adjudicar_automatico": "adjudicar_automatico"
    })
    g.add_edge("supervisar_sobreprecio", END)
    g.add_edge("adjudicar_automatico", END)

    return g.compile(checkpointer=InMemorySaver())
