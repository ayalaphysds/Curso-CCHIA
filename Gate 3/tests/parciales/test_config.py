"""Pruebas parciales aisladas de servicio/config.py usando monkeypatch (Bloque 39)."""

import pytest

from servicio import config


def test_config_valores_por_defecto(monkeypatch):
    for var in ("ENTORNO", "MODELO", "PERMITIR_RESPALDO", "GEMINI_API_KEY", "UMBRAL_SOBREPRECIO_PCT"):
        monkeypatch.delenv(var, raising=False)
    assert config.entorno() == "desarrollo"
    assert config.modelo_solicitado() == "simulado"
    assert config.permitir_respaldo() is False
    assert config.modelo_configurado() is False
    assert config.umbral_sobreprecio_pct() == 15.0


def test_config_clave_faltante_lanza_error_diferido(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(config.ConfiguracionIncompleta):
        config.clave_modelo()


def test_contrato_config_lee_valores_inyectados(monkeypatch):
    monkeypatch.setenv("ENTORNO", "pruebas")
    monkeypatch.setenv("MODELO", "real")
    monkeypatch.setenv("PERMITIR_RESPALDO", "1")
    monkeypatch.setenv("UMBRAL_SOBREPRECIO_PCT", "12.5")
    assert config.entorno() == "pruebas"
    assert config.modelo_solicitado() == "real"
    assert config.permitir_respaldo() is True
    assert config.umbral_sobreprecio_pct() == 12.5
