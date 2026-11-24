"""Pruebas parciales aisladas de servicio/recuperador.py (Bloques 39 y 45)."""

from servicio.contratos import Fragmento, verificar_fragmento
from servicio.recuperador import recuperar


def test_recuperar_paracetamol_encuentra_catalogo():
    frags = recuperar("Cual es el precio de referencia del Paracetamol 500 mg?", k=3)
    assert len(frags) >= 1
    assert any(f.fuente == "cenabast_catalogo_precios_referencia_2026.md" for f in frags)
    assert any("22.40" in f.texto for f in frags)


def test_recuperar_fuera_de_dominio_retorna_vacio():
    assert recuperar("Cual es la temperatura en Marte hoy?", k=3) == []
    assert recuperar("   ", k=3) == []


def test_contrato_fragmentos_respetan_esquema():
    frags = recuperar("Cuales son las multas por atraso en entrega ordinaria CENABAST?", k=2)
    assert 1 <= len(frags) <= 2
    for frag in frags:
        assert isinstance(verificar_fragmento(frag), Fragmento)
        assert frag.fuente.endswith(".md")
        assert frag.puntaje > 0


def test_limitacion_lim_02_otro_idioma_y_sinonimos():
    """Fija la limitacion conocida LIM-02: consultas en ingles o sinonimos coloquiales no recuperan."""
    assert recuperar("What is the reference price of acetaminophen?", k=3) == []
    assert recuperar("cuanto sale el remedio para bajar la fiebre?", k=3) == []
