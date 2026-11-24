"""Pruebas unitarias de verificar_decisiones.py (Bloque 45.3)."""

import verificar_decisiones as vd


def test_cargar_decisiones_lee_al_menos_cinco():
    decs = vd.cargar_decisiones()
    assert len(decs) >= 5
    for d in decs:
        for campo in vd.CAMPOS:
            assert d["campos"].get(campo), f"{d['id']} sin {campo}"


def test_cargar_limitaciones_lee_tabla_seis_columnas():
    lims = vd.cargar_limitaciones()
    assert len(lims) >= 3
    ids = [l["id"] for l in lims]
    assert "LIM-01" in ids and "LIM-02" in ids and "LIM-03" in ids


def test_declaradas_incluye_ataques_alucinaciones_matriz_y_transferencia():
    dec = vd.declaradas()
    assert "ataques:A-07" in dec
    assert "alucinaciones:H-04" in dec
    assert "alucinaciones:H-05" in dec
    assert "matriz_modelo:MP-08" in dec
    assert "transferencia:T-05" in dec
    assert "transferencia:T-06" in dec


def test_origenes_limitaciones_coinciden_exactamente_con_codigo():
    lims = vd.cargar_limitaciones()
    doc_set = {p.strip() for l in lims for p in l["origen"].split(",") if p.strip()}
    assert doc_set == vd.declaradas()


def test_decisiones_tienen_costos_y_alternativas_extensos():
    for d in vd.cargar_decisiones():
        assert len(d["campos"]["Alternativas descartadas"]) >= vd.MIN_TEXTO
        assert len(d["campos"]["Costo"]) >= vd.MIN_TEXTO


def test_estados_de_decisiones_son_validos():
    for d in vd.cargar_decisiones():
        assert d["campos"]["Estado"] in ("vigente", "reemplazada")


def test_verificador_decisiones_retorna_cero():
    assert vd.main() == 0
