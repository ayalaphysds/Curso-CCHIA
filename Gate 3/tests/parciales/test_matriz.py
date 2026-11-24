"""Pruebas unitarias de ejecutar_matriz.py (Bloque 42.3)."""

import ejecutar_matriz as em


def test_motivos_de_falla_vacio_cuando_todo_coincide():
    esp = {"estado": 200, "contiene": ["22.40"], "fuentes": ["doc.md"]}
    assert em.motivos_de_falla(esp, 200, "Precio 22.40", {"fuentes": ["doc.md"]}) == []


def test_motivos_de_falla_detecta_estado_incorrecto():
    esp = {"estado": 200, "contiene": ["ok"]}
    motivos = em.motivos_de_falla(esp, 404, "ok")
    assert any("estado" in m for m in motivos)


def test_motivos_de_falla_detecta_texto_faltante_y_prohibido():
    esp = {"estado": 200, "contiene": ["esperado"], "no_contiene": ["Traceback"]}
    motivos = em.motivos_de_falla(esp, 200, "Traceback error")
    assert len(motivos) == 2


def test_motivos_de_falla_verifica_fuentes_vacias():
    esp = {"estado": 200, "contiene": ["sin info"], "fuentes": []}
    motivos = em.motivos_de_falla(esp, 200, "sin info", {"fuentes": ["algo.md"]})
    assert any("vacias" in m for m in motivos)


def test_huella_es_determinista_y_cambia_al_editar():
    m1 = [{"id": "MP-01", "estado": 200}]
    m2 = [{"id": "MP-01", "estado": 404}]
    assert em.huella(m1) == em.huella(m1)
    assert len(em.huella(m1)) == 12
    assert em.huella(m1) != em.huella(m2)


def test_contrato_los_motivos_son_una_lista_de_textos():
    esp = {"estado": 200, "contiene": ["abc"]}
    res = em.motivos_de_falla(esp, 500, "xyz")
    assert isinstance(res, list)
    assert all(isinstance(x, str) for x in res)
