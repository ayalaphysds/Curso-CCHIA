"""Pruebas parciales del mecanismo de respaldo servicio/respaldo.py (Bloque 41)."""

import pytest

from servicio import respaldo
from servicio.errores import ModeloNoDisponibleError


def test_respaldo_en_modo_simulado(monkeypatch):
    monkeypatch.setenv("MODELO", "simulado")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    modelo, modo, aviso = respaldo.elegir_modelo()
    assert modelo.nombre == "simulado"
    assert modo == "simulado"
    assert aviso is None


def test_modelo_real_sin_clave_y_sin_respaldo_falla_honestamente(monkeypatch):
    monkeypatch.setenv("MODELO", "real")
    monkeypatch.setenv("PERMITIR_RESPALDO", "0")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ModeloNoDisponibleError):
        respaldo.elegir_modelo()


def test_modelo_real_sin_clave_con_respaldo_declara_advertencia(monkeypatch):
    monkeypatch.setenv("MODELO", "real")
    monkeypatch.setenv("PERMITIR_RESPALDO", "1")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    modelo, modo, aviso = respaldo.elegir_modelo()
    assert modelo.nombre == "simulado"
    assert modo == "respaldo"
    assert aviso is not None and "respaldo" in aviso.lower()
