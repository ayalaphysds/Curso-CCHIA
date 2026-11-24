"""Pruebas parciales aisladas de servicio/prompt.py (Bloque 39)."""

import pytest

from servicio.contratos import Fragmento
from servicio.prompt import HUELLA_PROMPT, INSTRUCCION, VERSION_PROMPT, construir_prompt


def _frag_demo() -> Fragmento:
    return Fragmento(
        fuente="cenabast_catalogo_precios_referencia_2026.md",
        seccion="Registro de medicamento - Catalogo 2026",
        texto="| **51181504** | **PARACETAMOL 500 MG** | Comprimido oral | Unidad | **$22.40 CLP** | $20.00 - $25.00 CLP | 145.000.000 |",
        puntaje=8.0,
    )


def test_construir_prompt_incluye_instruccion_contexto_y_pregunta():
    p = construir_prompt("Precio del Paracetamol?", [_frag_demo()])
    assert INSTRUCCION in p
    assert VERSION_PROMPT in p
    assert HUELLA_PROMPT in p
    assert "cenabast_catalogo_precios_referencia_2026.md" in p
    assert "Precio del Paracetamol?" in p


def test_construir_prompt_rechaza_entradas_vacias():
    with pytest.raises(ValueError):
        construir_prompt("   ", [_frag_demo()])
    with pytest.raises(ValueError):
        construir_prompt("Precio del Paracetamol?", [])


def test_contrato_prompt_es_texto_con_huella_hex():
    p = construir_prompt("Consulta sobre Paracetamol", [_frag_demo()])
    assert isinstance(p, str)
    assert len(HUELLA_PROMPT) == 12
    assert "CONTEXTO OFICIAL CENABAST:" in p
