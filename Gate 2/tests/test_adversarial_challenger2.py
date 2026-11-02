"""
Suite de Pruebas Adversariales - Challenger 2 (Milestone 3 / Gate 2).
Enfoque: Estrés de Supervisión Humana (LangGraph) y Verificación de Citación / Fallback RAG.

Objetivo:
1. Evaluar escenarios de borde en LangGraph: sobreprecio extremo (+500%), umbrales exactos (20.0% vs 20.1%),
   desviación negativa (-30%), rechazo humano explícito y aislamiento por thread_id.
2. Evaluar fidelidad de citación en consultas reales de catálogo CENABAST.
3. Evaluar comportamiento adversarial ante consultas fuera del corpus (repuestos automotrices, capital de Francia,
   fármacos no catalogados como Ibuprofeno) para verificar fallback controlado sin alucinación de citas.
"""

import os
import sys
import re
import pytest

# Asegurar path de importación de Gate 2
directorio_gate2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_gate2 not in sys.path:
    sys.path.insert(0, directorio_gate2)

from langgraph.types import Command
from servicio_rag import ejecutar_servicio
from src.supervision import crear_supervision, crear_grafo_supervision_precios
from src.recuperador import RESPUESTA_SIN_CONTEXTO

DIRECTORIO_DATA = os.path.join(directorio_gate2, "data")
ARCHIVOS_CORPUS = set(os.listdir(DIRECTORIO_DATA))


# =============================================================================
# BLOQUE 1: ESTRÉS DE SUPERVISIÓN HUMANA (LANGGRAPH)
# =============================================================================

class TestEstresSupervisionHumana:
    """Pruebas adversariales sobre el grafo de supervisión interactiva LangGraph."""

    def test_sobreprecio_extremo_500_pct_pausa_y_reanuda(self):
        """Sobreprecio exorbitante (+500%) debe pausar y reanudarse fielmente con Command(resume=True)."""
        app = crear_grafo_supervision_precios()
        cfg = {"configurable": {"thread_id": "adv-extremo-500"}}
        entrada = {
            "medicamento": "Ceftriaxona 1g",
            "precio_ofertado": 7500.0,
            "precio_referencia": 1250.0,  # +500%
            "desviacion_pct": 0.0,
            "requiere_supervision": False,
            "aprobado": None,
            "dictamen": "",
        }
        pausado = app.invoke(entrada, config=cfg)
        assert "__interrupt__" in pausado, "Debe pausarse ante sobreprecio de +500%"
        assert pausado["__interrupt__"][0].value["desviacion_pct"] == 500.0

        resuelto = app.invoke(Command(resume=True), config=cfg)
        assert resuelto["aprobado"] is True
        assert resuelto["desviacion_pct"] == 500.0
        assert "autorizada por excepción" in resuelto["dictamen"]

    def test_umbral_exacto_20_0_pct_no_pausa(self):
        """Desviación exactamente en el límite de 20.0% no debe pausar (adjudicación automática)."""
        app = crear_grafo_supervision_precios()
        cfg = {"configurable": {"thread_id": "adv-umbral-20-0"}}
        entrada = {
            "medicamento": "Losartán 50mg",
            "precio_ofertado": 120.0,
            "precio_referencia": 100.0,  # exactamente 20.0%
            "desviacion_pct": 0.0,
            "requiere_supervision": False,
            "aprobado": None,
            "dictamen": "",
        }
        resuelto = app.invoke(entrada, config=cfg)
        assert "__interrupt__" not in resuelto, "20.0% exacto no debe activar interrupción"
        assert resuelto["aprobado"] is True
        assert "Adjudicación estándar" in resuelto["dictamen"]

    def test_umbral_exacto_20_1_pct_activa_interrupcion(self):
        """Desviación de 20.1% (> 20.0%) debe pausar inmediatamente el flujo."""
        app = crear_grafo_supervision_precios()
        cfg = {"configurable": {"thread_id": "adv-umbral-20-1"}}
        entrada = {
            "medicamento": "Losartán 50mg",
            "precio_ofertado": 120.1,
            "precio_referencia": 100.0,  # 20.1%
            "desviacion_pct": 0.0,
            "requiere_supervision": False,
            "aprobado": None,
            "dictamen": "",
        }
        pausado = app.invoke(entrada, config=cfg)
        assert "__interrupt__" in pausado, "20.1% debe activar interrupción humana"
        assert pausado["__interrupt__"][0].value["desviacion_pct"] == 20.1

    def test_desviacion_negativa_30_pct_adjudicacion_automatica(self):
        """Desviación favorable (-30.0%) no requiere supervisión y adjudica automáticamente."""
        app = crear_grafo_supervision_precios()
        cfg = {"configurable": {"thread_id": "adv-negativa-30"}}
        entrada = {
            "medicamento": "Paracetamol 500mg",
            "precio_ofertado": 70.0,
            "precio_referencia": 100.0,  # -30.0%
            "desviacion_pct": 0.0,
            "requiere_supervision": False,
            "aprobado": None,
            "dictamen": "",
        }
        resuelto = app.invoke(entrada, config=cfg)
        assert "__interrupt__" not in resuelto
        assert resuelto["aprobado"] is True
        assert resuelto["desviacion_pct"] == -30.0

    def test_rechazo_humano_explicito_fija_aprobado_false(self):
        """Tanto el grafo de prompt como el de precios deben registrar aprobado=False ante rechazo."""
        # 1. Grafo oficial de supervisión de despliegue
        app1, entrada1 = crear_supervision()
        cfg1 = {"configurable": {"thread_id": "adv-rechazo-prompt"}}
        app1.invoke(entrada1, config=cfg1)
        res1 = app1.invoke(Command(resume=False), config=cfg1)
        assert res1["aprobado"] is False
        assert "Rechazado" in res1["motivo"]

        # 2. Grafo de supervisión de sobreprecio
        app2 = crear_grafo_supervision_precios()
        cfg2 = {"configurable": {"thread_id": "adv-rechazo-precio"}}
        entrada2 = {
            "medicamento": "Insulina Humana",
            "precio_ofertado": 5000.0,
            "precio_referencia": 3800.0,  # +31.58%
            "desviacion_pct": 0.0,
            "requiere_supervision": False,
            "aprobado": None,
            "dictamen": "",
        }
        app2.invoke(entrada2, config=cfg2)
        res2 = app2.invoke(Command(resume=False), config=cfg2)
        assert res2["aprobado"] is False
        assert "RECHAZADA" in res2["dictamen"]

    def test_persistencia_thread_id_y_ausencia_de_loops(self):
        """Verifica que dos hilos independientes no interfieran y que no existan ciclos infinitos."""
        app = crear_grafo_supervision_precios()
        cfgA = {"configurable": {"thread_id": "thread-audit-A"}}
        cfgB = {"configurable": {"thread_id": "thread-audit-B"}}

        entA = {"medicamento": "Med A", "precio_ofertado": 150.0, "precio_referencia": 100.0, "desviacion_pct": 0.0, "requiere_supervision": False, "aprobado": None, "dictamen": ""}
        entB = {"medicamento": "Med B", "precio_ofertado": 160.0, "precio_referencia": 100.0, "desviacion_pct": 0.0, "requiere_supervision": False, "aprobado": None, "dictamen": ""}

        app.invoke(entA, config=cfgA)
        app.invoke(entB, config=cfgB)

        stateA = app.get_state(cfgA)
        stateB = app.get_state(cfgB)
        assert stateA.values["medicamento"] == "Med A"
        assert stateB.values["medicamento"] == "Med B"

        resA = app.invoke(Command(resume=True), config=cfgA)
        resB = app.invoke(Command(resume=False), config=cfgB)

        assert resA["aprobado"] is True
        assert resB["aprobado"] is False


# =============================================================================
# BLOQUE 2: FIDELIDAD DE CITACIÓN EN CONSULTAS REALES DEL CORPUS
# =============================================================================

class TestFidelidadCitacionCorpusReal:
    """Verifica que en consultas reales de CENABAST las citas apunten a archivos existentes."""

    @pytest.mark.parametrize("consulta,farmaco_o_tema,archivo_esperado", [
        ("¿Cuál es el precio de referencia del Paracetamol 500mg?", "Paracetamol", "cenabast_catalogo_precios_referencia_2026.md"),
        ("¿Cuál es el precio de referencia de la Amoxicilina 500mg?", "Amoxicilina", "cenabast_catalogo_precios_referencia_2026.md"),
        ("¿Cuál es el valor referencial de la Insulina Humana NPH?", "Insulina", "cenabast_catalogo_precios_referencia_2026.md"),
        ("¿Cuáles son las multas por atraso según las bases de licitación?", "multa", "cenabast_bases_licitacion_medicamentos.md"),
    ])
    def test_consulta_real_cita_archivo_existente(self, consulta, farmaco_o_tema, archivo_esperado):
        respuesta, fuentes = ejecutar_servicio(consulta, mock=True)
        assert fuentes, f"No se obtuvieron fuentes para '{consulta}'"
        
        # Verificar que todos los nombres en 'fuentes' existan en Gate 2/data/
        for f in fuentes:
            assert f in ARCHIVOS_CORPUS, f"La fuente '{f}' no existe físicamente en Gate 2/data/"

        # Extraer etiquetas de cita textual [fuente: <doc>]
        citas_en_texto = re.findall(r"\[fuente:\s*([^\]]+)\]", respuesta)
        assert len(citas_en_texto) > 0, f"La respuesta no contiene etiquetas [fuente: ...]: {respuesta}"

        for c in citas_en_texto:
            assert c in ARCHIVOS_CORPUS, f"La cita '[fuente: {c}]' no corresponde a un archivo en data/"


# =============================================================================
# BLOQUE 3: ESTRÉS DE CITACIÓN Y FALLBACK RAG ANTE CONSULTAS FUERA DE CORPUS
# =============================================================================

class TestFallbackConsultasFueraDeCorpus:
    """
    Prueba crítica adversarial:
    Cuando el usuario pregunta sobre temas ajenos al corpus (repuestos automotrices, capital de Francia,
    o medicamentos inexistentes), el sistema DEBE responder con el fallback controlado:
        'No tengo informacion suficiente y verificada para responder esto.'
    Y NO debe alucinar afirmaciones de precios ni citas documentales indebidas.
    """

    @pytest.mark.parametrize("consulta_ajena", [
        "¿Cuáles son los precios de repuestos automotrices para camionetas?",
        "¿Cuál es la capital de Francia?",
        "¿Cuál es el precio de referencia del Ibuprofeno 400mg según el catálogo?",
    ])
    def test_consulta_ajena_activa_fallback_sin_alucinacion(self, consulta_ajena):
        respuesta, fuentes = ejecutar_servicio(consulta_ajena, mock=True)
        
        # Debe retornar la respuesta de fallback controlada
        assert respuesta == RESPUESTA_SIN_CONTEXTO, (
            f"Para la consulta ajena '{consulta_ajena}', el sistema respondió:\n"
            f"'{respuesta}'\n"
            f"en lugar de emitir el fallback controlado: '{RESPUESTA_SIN_CONTEXTO}'"
        )

        # No debe citar fuentes para una consulta sin respaldo
        assert fuentes == [], (
            f"Para la consulta ajena '{consulta_ajena}', el sistema devolvió fuentes espurias: {fuentes}"
        )
