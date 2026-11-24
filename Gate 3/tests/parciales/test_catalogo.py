"""Pruebas parciales aisladas de servicio/catalogo.py (Bloque 39)."""

from servicio.catalogo import consultar_licitacion, evaluar_precio


def test_evaluar_precio_clasifica_umbrales_cenabast(monkeypatch):
    monkeypatch.setenv("UMBRAL_SOBREPRECIO_PCT", "15.0")
    comp = evaluar_precio("51181504", 23.0)
    neg = evaluar_precio("51181504", 25.0)
    crit = evaluar_precio("51181504", 33.6)
    tem = evaluar_precio("51101506", 25.0)

    assert comp["categoria"] == "COMPETITIVO" and comp["requiere_supervision"] is False
    assert neg["categoria"] == "NEGOCIACION" and neg["requiere_supervision"] is False
    assert crit["categoria"] == "SOBREPRECIO_CRITICO" and crit["requiere_supervision"] is True
    assert tem["categoria"] == "TEMERARIO" and tem["requiere_supervision"] is True


def test_catalogo_codigo_o_licitacion_inexistente_retorna_none():
    assert evaluar_precio("51999999", 100.0) is None
    assert consultar_licitacion("LIC-999") is None


def test_contrato_evaluar_precio_y_licitacion_retornan_campos_requeridos():
    res = evaluar_precio("51181504", 33.6)
    assert set(res.keys()) == {
        "codigo_onu", "medicamento", "precio_referencia", "precio_ofertado",
        "desviacion_pct", "categoria", "requiere_supervision", "recomendacion", "fuente",
    }
    lic = consultar_licitacion("LIC-723")
    assert lic is not None and lic["estado"] == "RECHAZAR"
