"""Pruebas parciales aisladas de servicio/modelo.py (Bloque 39)."""

from servicio.contratos import Fragmento
from servicio.modelo import ModeloSimulado


def test_modelo_simulado_cita_fuente_y_precio():
    frag = Fragmento(
        fuente="cenabast_catalogo_precios_referencia_2026.md",
        seccion="Registro de medicamento - Catalogo 2026",
        texto="| **51181504** | **PARACETAMOL 500 MG** | Comprimido oral | Unidad | **$22.40 CLP** | $20.00 - $25.00 CLP | 145.000.000 |",
        puntaje=10.0,
    )
    modelo = ModeloSimulado()
    resp = modelo.generar("prompt", pregunta="Precio Paracetamol?", fragmentos=[frag])
    assert "$22.40 CLP" in resp
    assert "[fuente: cenabast_catalogo_precios_referencia_2026.md]" in resp


def test_modelo_simulado_sin_fragmentos_se_abstiene():
    modelo = ModeloSimulado()
    resp = modelo.generar("prompt", pregunta="Cualquier cosa", fragmentos=[])
    assert "No encuentro esa informacion" in resp


def test_contrato_modelo_simulado_retorna_str_y_tiene_nombre():
    modelo = ModeloSimulado()
    assert modelo.nombre == "simulado"
    frag = Fragmento(
        fuente="cenabast_bases_licitacion_medicamentos.md",
        seccion="UMBRALES DE DESVIACIÓN",
        texto="Sobreprecio Crítico (Desviación > 15.0%): prohibida la adjudicación automatizada.",
        puntaje=5.0,
    )
    out = modelo.generar("p", pregunta="sobreprecio umbral", fragmentos=[frag])
    assert isinstance(out, str) and len(out) > 20
    assert "[fuente: cenabast_bases_licitacion_medicamentos.md]" in out
