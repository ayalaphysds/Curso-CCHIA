"""
Pruebas Unitarias de Recuperación, Citación y Métricas de Calidad (Gate 2).
Especialización en IA Accenture - Curso CCHIA
"""

import os
import sys
import pytest
from langchain_core.documents import Document

directorio_gate2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_gate2 not in sys.path:
    sys.path.insert(0, directorio_gate2)

from src.recuperador import (
    formatear_contexto,
    extraer_lista_fuentes,
    armar_prompt_rag,
    recuperar_documentos,
    RESPUESTA_SIN_CONTEXTO,
)
from src.evaluador import (
    calcular_metricas_recuperacion,
    verificar_citas_en_respuesta,
    calcular_costo_y_latencia,
)
from src.indexador import crear_o_cargar_indice


class TestRecuperacionGate2:
    """Pruebas del pipeline de recuperación y formateo con fuentes."""

    def test_formatear_contexto_incluye_etiqueta_fuente(self):
        docs = [
            Document(page_content="Precio Paracetamol: $12 CLP.", metadata={"fuente": "catalogo_2026.md"}),
            Document(page_content="Multa por atraso: 0.5% diario.", metadata={"fuente": "bases_2026.md"}),
        ]
        contexto = formatear_contexto(docs)
        assert "[fuente: catalogo_2026.md]" in contexto
        assert "[fuente: bases_2026.md]" in contexto
        assert "Precio Paracetamol" in contexto

    def test_extraer_lista_fuentes_univoca_y_ordenada(self):
        docs = [
            Document(page_content="a", metadata={"fuente": "b_doc.md"}),
            Document(page_content="b", metadata={"fuente": "a_doc.md"}),
            Document(page_content="c", metadata={"fuente": "b_doc.md"}),
        ]
        fuentes = extraer_lista_fuentes(docs)
        assert fuentes == ["a_doc.md", "b_doc.md"]

    def test_armar_prompt_rag_contiene_reglas_y_contexto(self):
        pregunta = "¿Cuál es el valor referencial?"
        contexto = "[fuente: catalogo.md] El valor es $100."
        fuentes = ["catalogo.md"]
        prompt = armar_prompt_rag(pregunta, contexto, fuentes)
        assert "[fuente: <nombre_archivo>]" in prompt
        assert RESPUESTA_SIN_CONTEXTO in prompt
        assert contexto in prompt
        assert pregunta in prompt

    def test_calcular_metricas_recuperacion_precision_recall(self):
        recuperados = [
            Document(page_content="d1", metadata={"fuente": "cenabast_catalogo.md"}),
            Document(page_content="d2", metadata={"fuente": "cenabast_bases.md"}),
            Document(page_content="d3", metadata={"fuente": "otro.md"}),
        ]
        esperadas = ["cenabast_catalogo.md", "cenabast_bases.md"]
        metricas = calcular_metricas_recuperacion(recuperados, esperadas)
        assert metricas["precision"] == pytest.approx(2 / 3, 0.01)
        assert metricas["recall"] == pytest.approx(1.0, 0.01)
        assert metricas["f1"] > 0.7

    def test_verificar_citas_en_respuesta(self):
        resp_con_cita = "El valor del producto es $12 [fuente: catalogo.md]."
        fuentes = ["catalogo.md", "bases.md"]
        res = verificar_citas_en_respuesta(resp_con_cita, fuentes)
        assert res["tiene_citas"] is True
        assert "catalogo.md" in res["citas_encontradas"]
        assert res["cobertura"] == 0.5

        resp_sin_cita = "El valor del producto es $12 sin especificar origen."
        res_sin = verificar_citas_en_respuesta(resp_sin_cita, fuentes)
        assert res_sin["tiene_citas"] is False
        assert res_sin["cobertura"] == 0.0

    def test_calcular_costo_y_latencia(self):
        telemetria = calcular_costo_y_latencia(duracion_ms=125.5, input_tokens=400, output_tokens=100)
        assert telemetria["duracion_ms"] == 125.5
        assert telemetria["input_tokens"] == 400
        assert telemetria["output_tokens"] == 100
        assert telemetria["costo_usd"] > 0
        assert telemetria["costo_clp"] > 0
