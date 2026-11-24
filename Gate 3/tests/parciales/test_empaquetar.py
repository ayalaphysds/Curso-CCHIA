"""Pruebas parciales aisladas de servicio/contratos.py (Bloque 39)."""

import pytest

from servicio.contratos import ContratoInvalido, empaquetar_respuesta


def test_empaquetar_deduplica_fuentes_preservando_orden():
    res = empaquetar_respuesta(
        respuesta="Precio $22.40 [fuente: a.md].",
        fuentes=["a.md", "b.md", "a.md"],
        trace_id="trace-12345678",
        modo_modelo="simulado",
    )
    assert res["fuentes"] == ["a.md", "b.md"]
    assert res["advertencia_respaldo"] is None


def test_empaquetar_rechaza_respuesta_o_modo_invalido():
    with pytest.raises(ContratoInvalido):
        empaquetar_respuesta("   ", [], "trace-1", "simulado")
    with pytest.raises(ContratoInvalido):
        empaquetar_respuesta("ok", [], "trace-1", "inventado")


def test_contrato_empaquetar_retorna_claves_exactas():
    res = empaquetar_respuesta("ok", ["doc.md"], "trace-abcd", "respaldo", "aviso")
    assert set(res.keys()) == {"respuesta", "fuentes", "trace_id", "modo_modelo", "advertencia_respaldo"}
    assert res["modo_modelo"] == "respaldo"
    assert res["advertencia_respaldo"] == "aviso"
