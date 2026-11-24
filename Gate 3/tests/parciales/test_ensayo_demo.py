"""Pruebas unitarias de ensayo_demo.py sin levantar servidores (Bloque S2.3)."""

import ensayo_demo as ed


def test_evaluar_aprueba_respuesta_valida_en_tiempo():
    paso = ed.PASOS[0]
    ok, _ = ed.evaluar(paso, 200, '{"estado":"ok","modelo_activo":"simulado"}', 0.12)
    assert ok is True


def test_evaluar_rechaza_estado_incorrecto_o_latencia_excedida():
    paso = ed.PASOS[0]
    assert ed.evaluar(paso, 500, '{"modelo_activo":"simulado"}', 0.10)[0] is False
    assert ed.evaluar(paso, 200, '{"modelo_activo":"simulado"}', 3.50)[0] is False


def test_tiempo_total_cabe_en_dos_minutos():
    ok, total, desglose = ed.tiempo_total(1.5)
    assert ok is True
    assert total <= 120.0
    assert desglose["manos"] == len(ed.PASOS) * ed.SEGUNDOS_POR_PASO


def test_ensayar_falla_limpiamente_si_servidor_no_arranca(monkeypatch):
    monkeypatch.setattr(ed, "puerto_libre", lambda _p: True)
    resultados, registros = ed.ensayar(arrancador=lambda _p, _m: None)
    assert registros == []
    assert resultados[0][0] == "ARRANQUE" and resultados[0][1] is False
