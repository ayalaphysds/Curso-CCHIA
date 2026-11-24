"""Pruebas parciales del detector de alucinaciones servicio/fundamentacion.py (Bloque 43)."""

from servicio.cadena import SIN_INFORMACION
from servicio.contratos import Fragmento
from servicio.fundamentacion import problemas_de_respaldo


def _frag_paracetamol() -> list[Fragmento]:
    return [
        Fragmento(
            fuente="cenabast_catalogo_precios_referencia_2026.md",
            seccion="Catalogo 2026",
            texto="PARACETAMOL 500 MG mediana $22.40 CLP rango $20.00 - $25.00 CLP. Sobreprecio Critico (> 15.0%): prohibida la adjudicacion automatizada.",
            puntaje=9.0,
        )
    ]


def test_respuesta_fundamentada_sin_problemas():
    resp = "Paracetamol 500 mg tiene precio de referencia $22.40 CLP [fuente: cenabast_catalogo_precios_referencia_2026.md]."
    assert problemas_de_respaldo(resp, _frag_paracetamol(), SIN_INFORMACION) == []


def test_detecta_fuente_inventada_y_cifra_falsa():
    resp = "Paracetamol cuesta $99.90 CLP [fuente: resolucion_falsa_2027.pdf]."
    probs = problemas_de_respaldo(resp, _frag_paracetamol(), SIN_INFORMACION)
    assert "H-FUENTE-INVENTADA" in probs
    assert "H-CIFRA-NO-RESPALDADA" in probs


def test_detecta_contradiccion_de_politica_critica():
    resp = "Aunque hay sobreprecio de 15.0%, se puede adjudicar automaticamente [fuente: cenabast_catalogo_precios_referencia_2026.md]."
    probs = problemas_de_respaldo(resp, _frag_paracetamol(), SIN_INFORMACION)
    assert "H-CONTRADICCION" in probs


def test_abstencion_siempre_es_valida():
    assert problemas_de_respaldo(SIN_INFORMACION, _frag_paracetamol(), SIN_INFORMACION) == []
