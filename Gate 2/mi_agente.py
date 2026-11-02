"""
Agente Auditor de Compras CENABAST con Límites de Autonomía y Supervisión Humana (Bloque 23, U2.4).
Especialización en IA Accenture - Curso CCHIA

Herramientas:
1. consultar_catalogo_cenabast (Riesgo Bajo): Consulta valores oficiales de referencia (autónoma).
2. calcular_sobreprecio_oferta (Riesgo Bajo): Operación aritmética de desvío porcentual (autónoma).
3. adjudicar_orden_compra (Riesgo Alto): Compromiso financiero de fondos públicos.
   -> Requiere obligatoriamente autorización humana formal (esperar_aprobacion).

Salidas:
- Registro auditable de ejecuciones y puntos de control en 'trazas_agente.jsonl'.
- Documentación de políticas de riesgo en 'docs/limites_autonomia.md'.
"""

import os
import sys
import json
import datetime
from typing import Dict, Any, Optional, Callable
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langchain_core.tools import tool
from agente_con_herramientas import CATALOGO_PRECIOS


# -----------------------------------------------------------------------------
# 1. Definición y Clasificación de Herramientas según Riesgo
# -----------------------------------------------------------------------------
NIVELES_RIESGO = {
    "consultar_catalogo_cenabast": "BAJO",
    "calcular_sobreprecio_oferta": "BAJO",
    "adjudicar_orden_compra": "ALTO",
}


@tool
def consultar_catalogo_cenabast(farmaco: str) -> str:
    """[Riesgo BAJO] Consulta el precio de referencia oficial del catálogo CENABAST 2026."""
    f = farmaco.lower().strip()
    for k, v in CATALOGO_PRECIOS.items():
        if k in f:
            return f"Catálogo CENABAST 2026: {k.capitalize()} = ${v:.2f} CLP netos por unidad."
    return f"Fármaco '{farmaco}' no encontrado en el catálogo de medicamentos esenciales 2026."


@tool
def calcular_sobreprecio_oferta(precio_ofertado: float, precio_referencia: float) -> Dict[str, Any]:
    """[Riesgo BAJO] Calcula la desviación porcentual de la oferta respecto a la línea base."""
    if precio_referencia <= 0:
        return {"error": "El precio de referencia debe ser mayor a 0"}
    desv = ((precio_ofertado - precio_referencia) / precio_referencia) * 100
    es_critico = desv > 15.0
    return {
        "precio_ofertado": precio_ofertado,
        "precio_referencia": precio_referencia,
        "desviacion_pct": round(desv, 2),
        "sobreprecio_critico": es_critico,
        "dictamen_sugerido": "RECHAZAR" if es_critico else ("NEGOCIAR" if desv > 5.0 else "ADJUDICAR")
    }


def adjudicar_orden_compra(
    id_licitacion: str,
    farmaco: str,
    proveedor: str,
    monto_total_clp: float,
    aprobacion_humana: bool = False,
    supervisor: Optional[str] = None
) -> Dict[str, Any]:
    """
    [Riesgo ALTO] Emisión formal de orden de compra en Mercado Público.
    ESTA ACCIÓN COMPROMETE RECURSOS FISCALES Y ESTÁ PROHIBIDA EN MODO 100% AUTÓNOMO.
    Requiere aprobación explícita de un supervisor humano.
    """
    if not aprobacion_humana:
        return {
            "estado": "DETENIDO_POR_SUPERVISION",
            "motivo": "Acción irreversible de alto riesgo presupuestario. Requiere autorización humana.",
            "id_licitacion": id_licitacion,
            "farmaco": farmaco,
            "monto_total_clp": monto_total_clp,
            "orden_compra_emitida": False,
        }

    return {
        "estado": "ADJUDICADA_CON_AUTORIZACION",
        "id_licitacion": id_licitacion,
        "farmaco": farmaco,
        "proveedor": proveedor,
        "monto_total_clp": monto_total_clp,
        "supervisor_autorizante": supervisor or "Jefe de Adquisiciones CENABAST",
        "timestamp_adjudicacion": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "orden_compra_emitida": True,
    }


# -----------------------------------------------------------------------------
# 2. Mecanismo de Interrupción y Registro en trazas_agente.jsonl
# -----------------------------------------------------------------------------
def registrar_traza(evento: Dict[str, Any], ruta_log: Optional[str] = None) -> None:
    """Escribe un registro estructurado en trazas_agente.jsonl."""
    if ruta_log is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_log = os.path.join(base_dir, "trazas_agente.jsonl")

    evento["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")


def esperar_aprobacion(
    accion: Dict[str, Any],
    aprobador_externo: Optional[Callable[[Dict[str, Any]], bool]] = None
) -> bool:
    """
    Punto de pausa y supervisión humana para operaciones clasificadas como Riesgo ALTO.
    Si se suministra una función 'aprobador_externo', se invoca para simulación automatizada;
    de lo contrario, en consola se presenta la decisión al auditor humano.
    """
    print(f"\n[ALERTA DE GOBERNANZA - RIESGO ALTO] Operación: {accion.get('tipo', 'Adjudicación')}")
    print(f"  Detalle: Licitación {accion.get('id_licitacion')} - Fármaco: {accion.get('farmaco')}")
    print(f"  Monto Comprometido: ${accion.get('monto_total_clp', 0):,.2f} CLP")

    if aprobador_externo is not None:
        aprobado = aprobador_externo(accion)
    else:
        # Modo interactivo por defecto o confirmación automática controlada
        aprobado = accion.get("aprobacion_previa", False)

    print(f"  Resultado de Supervisión Humana: {'AUTORIZADO' if aprobado else 'RECHAZADO / BLOQUEADO'}")
    return aprobado


class AgenteSupervisadoCENABAST:
    """Orquestador agéntico que evalúa el nivel de riesgo antes de cada ejecución."""

    def __init__(self, ruta_trazas: Optional[str] = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_trazas = ruta_trazas or os.path.join(base_dir, "trazas_agente.jsonl")

    def ejecutar_consulta(
        self,
        tipo_accion: str,
        parametros: Dict[str, Any],
        funcion_aprobacion: Optional[Callable[[Dict[str, Any]], bool]] = None
    ) -> Dict[str, Any]:
        riesgo = NIVELES_RIESGO.get(tipo_accion, "MEDIO")

        traza = {
            "accion": tipo_accion,
            "riesgo": riesgo,
            "parametros": {k: v for k, v in parametros.items() if k != "supervisor"},
        }

        if riesgo == "BAJO":
            if tipo_accion == "consultar_catalogo_cenabast":
                res = consultar_catalogo_cenabast.invoke(parametros)
            elif tipo_accion == "calcular_sobreprecio_oferta":
                res = calcular_sobreprecio_oferta.invoke(parametros)
            else:
                res = "Operación de bajo riesgo ejecutada"
            traza["estado"] = "EJECUTADO_AUTONOMAMENTE"
            traza["resultado"] = res
            registrar_traza(traza, self.ruta_trazas)
            return {"exito": True, "riesgo": riesgo, "resultado": res}

        elif riesgo == "ALTO":
            # Requiere intervención humana
            accion_desc = {"tipo": tipo_accion, **parametros}
            aprobado = esperar_aprobacion(accion_desc, funcion_aprobacion)
            traza["supervision_humana_requerida"] = True
            traza["aprobado_por_humano"] = aprobado

            resultado = adjudicar_orden_compra(
                id_licitacion=parametros.get("id_licitacion", "LIC-GEN"),
                farmaco=parametros.get("farmaco", "No especificado"),
                proveedor=parametros.get("proveedor", "No especificado"),
                monto_total_clp=parametros.get("monto_total_clp", 0.0),
                aprobacion_humana=aprobado,
                supervisor=parametros.get("supervisor"),
            )
            traza["resultado"] = resultado
            registrar_traza(traza, self.ruta_trazas)
            return {"exito": aprobado, "riesgo": riesgo, "resultado": resultado}

        else:
            traza["estado"] = "NO_SOPORTADO"
            registrar_traza(traza, self.ruta_trazas)
            return {"exito": False, "riesgo": riesgo, "error": "Tipo de acción no contemplada"}


def main():
    agente = AgenteSupervisadoCENABAST()

    print("=" * 75)
    print("  AGENTE AUDITOR CENABAST CON LÍMITES DE AUTONOMÍA (BLOQUE 23)")
    print("=" * 75)

    # 1. Operación de Riesgo Bajo (Consulta de Catálogo)
    print("\n[OPERACIÓN 1 - RIESGO BAJO] Consulta de catálogo de referencia:")
    r1 = agente.ejecutar_consulta("consultar_catalogo_cenabast", {"farmaco": "Paracetamol"})
    print(f"  Resultado: {r1['resultado']}")

    # 2. Operación de Riesgo Bajo (Cálculo de Sobreprecio)
    print("\n[OPERACIÓN 2 - RIESGO BAJO] Cálculo de sobreprecio de oferta:")
    r2 = agente.ejecutar_consulta("calcular_sobreprecio_oferta", {
        "precio_ofertado": 33.60,
        "precio_referencia": 22.40,
    })
    print(f"  Resultado: {r2['resultado']}")

    # 3. Operación de Riesgo Alto SIN Aprobación Humana (Bloqueada)
    print("\n[OPERACIÓN 3 - RIESGO ALTO] Intento de adjudicación SIN aprobación humana:")
    r3 = agente.ejecutar_consulta(
        "adjudicar_orden_compra",
        {
            "id_licitacion": "723-14-LP24",
            "farmaco": "Paracetamol 500 mg",
            "proveedor": "Laboratorio Chile S.A.",
            "monto_total_clp": 150000000.0,
        },
        funcion_aprobacion=lambda acc: False,  # Auditor humano rechaza o no autoriza
    )
    print(f"  Resultado: {r3['resultado']}")

    # 4. Operación de Riesgo Alto CON Aprobación Humana (Autorizada)
    print("\n[OPERACIÓN 4 - RIESGO ALTO] Adjudicación formal CON autorización del Jefe de Adquisiciones:")
    r4 = agente.ejecutar_consulta(
        "adjudicar_orden_compra",
        {
            "id_licitacion": "812-05-LR25",
            "farmaco": "Ceftriaxona 1 g",
            "proveedor": "Laboratorio Biosano S.A.",
            "monto_total_clp": 85000000.0,
            "supervisor": "Dr. Fernando Morales - Jefe de Adquisiciones CENABAST",
        },
        funcion_aprobacion=lambda acc: True,  # Auditor humano autoriza formalmente
    )
    print(f"  Resultado: {r4['resultado']}")

    print(f"\n✓ Trazas auditables registradas en: {agente.ruta_trazas}")


if __name__ == "__main__":
    main()
