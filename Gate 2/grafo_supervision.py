"""
Grafo de Supervisión Humana con LangGraph (Bloque 32, U2.7).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Control Humano en Adjudicaciones con Sobreprecio Crítico

Cumplimiento Normativo (Criterio No Compensable 4 de Gate 2):
1. Punto de interrupción interactivo 'interrupt()' que detiene el flujo algorítmico cuando
   la desviación de precio excede el 15.0% sobre la línea base de catálogo.
2. Checkpointer 'InMemorySaver' para persistencia del estado transaccional durante la pausa.
3. Reanudación controlada mediante 'Command(resume=True)' (autorización) o 'Command(resume=False)' (rechazo).
"""

import sys
from typing import TypedDict, Optional, Dict, Any
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class EstadoAdjudicacion(TypedDict):
    """Estado compartido del grafo de auditoría y adjudicación farmacéutica."""
    medicamento: str
    precio_ofertado: float
    precio_referencia: float
    desviacion_pct: float
    requiere_supervision: bool
    aprobado: Optional[bool]
    resultado: str
    orden_emitida: bool


def nodo_evaluar_oferta(estado: EstadoAdjudicacion) -> Dict[str, Any]:
    """
    Nodo 1: Calcula la desviación porcentual objetiva respecto a la referencia de catálogo.
    Si la desviación supera el 15.0%, marca 'requiere_supervision = True'.
    """
    ref = estado["precio_referencia"]
    ofertado = estado["precio_ofertado"]
    desviacion = ((ofertado - ref) / ref) * 100 if ref > 0 else 0.0
    desv_redondeada = round(desviacion, 2)
    requiere = desv_redondeada > 15.0

    return {
        "desviacion_pct": desv_redondeada,
        "requiere_supervision": requiere,
    }


def enrutar_decision(estado: EstadoAdjudicacion) -> str:
    """Bifurcación condicional: si requiere supervisión va a 'solicitar_supervision', si no a 'adjudicar_directo'."""
    if estado.get("requiere_supervision", False):
        return "solicitar_supervision"
    return "adjudicar_directo"


def nodo_solicitar_supervision(estado: EstadoAdjudicacion) -> Dict[str, Any]:
    """
    Nodo 2 (Punto Crítico Human-in-the-Loop):
    Emite un interrupt() para congelar el estado en el checkpointer.
    Al reanudarse con Command(resume=True/False), procesa la decisión del supervisor humano.
    """
    datos_alerta = {
        "alerta": "SOBREPRECIO_CRITICO_CENABAST",
        "medicamento": estado["medicamento"],
        "precio_ofertado": estado["precio_ofertado"],
        "precio_referencia": estado["precio_referencia"],
        "desviacion_pct": estado["desviacion_pct"],
        "mensaje": "La desviación excede el 15.0%. Requiere autorización expresa del Jefe de Adquisiciones.",
    }

    # Interrupción interactiva de LangGraph
    decision_humana = interrupt(datos_alerta)

    # Reanudación con valor booleano tipado
    es_aprobado = bool(decision_humana is True)
    if es_aprobado:
        resultado = (
            f"Adjudicación autorizada mediante excepción formal de supervisión humana para {estado['medicamento']} "
            f"a ${estado['precio_ofertado']} CLP (+{estado['desviacion_pct']}%)."
        )
    else:
        resultado = (
            f"Adjudicación RECHAZADA por el supervisor humano. Sobreprecio de +{estado['desviacion_pct']}% "
            f"desestimado conforme a política de probidad fiscal."
        )

    return {
        "aprobado": es_aprobado,
        "resultado": resultado,
        "orden_emitida": es_aprobado,
    }


def nodo_adjudicar_directo(estado: EstadoAdjudicacion) -> Dict[str, Any]:
    """
    Nodo 3: Adjudicación automática en rango competitivo (desviación <= 15.0%).
    """
    return {
        "aprobado": True,
        "resultado": (
            f"Adjudicación ordinaria aprobada automáticamente para {estado['medicamento']} "
            f"con desviación competitiva de {estado['desviacion_pct']}%."
        ),
        "orden_emitida": True,
    }


def construir_grafo_supervision(checkpointer: Optional[Any] = None):
    """
    Compila el grafo de supervisión humana con checkpointer en memoria.
    """
    builder = StateGraph(EstadoAdjudicacion)

    builder.add_node("evaluar_oferta", nodo_evaluar_oferta)
    builder.add_node("solicitar_supervision", nodo_solicitar_supervision)
    builder.add_node("adjudicar_directo", nodo_adjudicar_directo)

    builder.add_edge(START, "evaluar_oferta")
    builder.add_conditional_edges(
        "evaluar_oferta",
        enrutar_decision,
        {
            "solicitar_supervision": "solicitar_supervision",
            "adjudicar_directo": "adjudicar_directo",
        }
    )
    builder.add_edge("solicitar_supervision", END)
    builder.add_edge("adjudicar_directo", END)

    saver = checkpointer if checkpointer is not None else InMemorySaver()
    return builder.compile(checkpointer=saver)


if __name__ == "__main__":
    print("=" * 75)
    print("  DEMOSTRACIÓN DEL GRAFO DE SUPERVISIÓN HUMANA LANGGRAPH (BLOQUE 32)")
    print("=" * 75)

    grafo = construir_grafo_supervision()
    config = {"configurable": {"thread_id": "sesion_demo_cenabast_001"}}

    # Caso: Paracetamol con sobreprecio del 50% ($33.60 vs $22.40)
    estado_inicial: EstadoAdjudicacion = {
        "medicamento": "Paracetamol 500 mg",
        "precio_ofertado": 33.60,
        "precio_referencia": 22.40,
        "desviacion_pct": 0.0,
        "requiere_supervision": False,
        "aprobado": None,
        "resultado": "",
        "orden_emitida": False,
    }

    print("\n[PASO 1] Iniciando evaluación algorítmica de la oferta:")
    eventos = list(grafo.stream(estado_inicial, config=config))
    print(f"  Eventos procesados antes de la pausa: {len(eventos)}")

    estado_actual = grafo.get_state(config)
    print(f"  ¿El grafo se encuentra en pausa por interrupción? {len(estado_actual.tasks) > 0}")
    if estado_actual.tasks:
        alerta = estado_actual.tasks[0].interrupts[0].value
        print(f"  Datos emitidos por interrupt():\n    {alerta}")

    # Reanudación con aprobación humana
    print("\n[PASO 2] Reanudando ejecución con autorización humana (Command(resume=True)):")
    eventos_reanudacion = list(grafo.stream(Command(resume=True), config=config))
    estado_final = grafo.get_state(config)
    print(f"  Estado Final Aprobado: {estado_final.values.get('aprobado')}")
    print(f"  Orden Emitida:         {estado_final.values.get('orden_emitida')}")
    print(f"  Dictamen Final:\n    {estado_final.values.get('resultado')}")
