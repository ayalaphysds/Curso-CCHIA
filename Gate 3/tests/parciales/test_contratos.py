"""Pruebas de contrato estructural entre capas (Bloque 39)."""

import pytest

from servicio.contratos import ContratoInvalido, Fragmento, verificar_fragmento


def test_verificar_fragmento_valido():
    f = Fragmento("doc.md", "sec", "contenido valido", 1.5)
    assert verificar_fragmento(f) == f


def test_verificar_fragmento_rechaza_tipos_y_vacios():
    with pytest.raises(ContratoInvalido):
        verificar_fragmento({"fuente": "doc.md"})
    with pytest.raises(ContratoInvalido):
        verificar_fragmento(Fragmento("", "sec", "texto", 1.0))
    with pytest.raises(ContratoInvalido):
        verificar_fragmento(Fragmento("doc.md", "sec", "texto", -1.0))
