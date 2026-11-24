"""Pruebas unitarias puras de rubrica_gate3.py y verificar_gate3.py (Bloque S2.3)."""

from pathlib import Path
import rubrica_gate3 as rg
import verificar_gate3 as vg


def test_pesos_rubrica_suman_cien():
    assert sum(c["peso"] for c in rg.CRITERIOS) == 100


def test_mapeo_uno_a_uno_entre_rubrica_y_fuentes():
    usadas_rubrica = {f for c in rg.CRITERIOS for f in c["fuentes"]} | {
        f for nc in rg.NO_COMPENSABLES for f in nc["fuentes"]
    }
    assert usadas_rubrica == set(vg.FUENTES.keys())


def test_todos_los_scripts_citados_en_fuentes_existen():
    for nombre, cmd in vg.FUENTES.items():
        if len(cmd) >= 2 and cmd[1].endswith(".py"):
            assert Path(cmd[1]).is_file(), f"Falta script para fuente {nombre}: {cmd[1]}"


def test_nota_anclas_oficiales():
    assert vg.nota(0) == 1.0
    assert vg.nota(60) == 4.0
    assert vg.nota(80) == 5.5
    assert vg.nota(100) == 7.0


def test_puntuar_sin_evidencia_da_cero_y_parcial_es_proporcional():
    _, pts_cero = vg.puntuar({})
    assert pts_cero == 0.0

    resultados = {"ficha": {"cumplidas": 5, "total": 5}, "decisiones": {"cumplidas": 0, "total": 7}}
    detalle, pts = vg.puntuar(resultados)
    c1 = next(c for c in detalle if c["id"] == "C1")
    assert c1["puntos"] == 5.0
    assert pts == 5.0


def test_fallo_no_compensable_anula_puntaje_alto():
    veredicto, _, rc = vg.decidir(95.0, [("NC-2", "falla servicio")], [])
    assert veredicto == "NO APRUEBA"
    assert rc == 1


def test_modo_sin_docker_retorna_provisional_codigo_dos():
    veredicto, _, rc = vg.decidir(100.0, [], ["stack", "ejecucion", "registro"])
    assert veredicto == "PROVISIONAL"
    assert rc == 2
