"""Pruebas unitarias de medir_guion.py sin invocacion recursiva de pytest (Bloque S2.2/S2.3)."""

from pathlib import Path
import medir_guion as mg


def test_identificador_ignora_codigo_pedido_o_licitacion():
    assert mg.IDENTIFICADOR.findall("Consultamos PED-1001 y LIC-723 sin conflicto con D-02 ni R-01") == [
        ("D", "02"),
        ("R", "01"),
    ]


def test_hablado_excluye_tablas_listas_y_encabezados():
    cuerpo = "# Titulo\nTexto hablado real.\n- PASO-1 Demo\n| 1 | a | b |\n```python\nx=1\n```\nMas texto."
    assert mg.hablado(cuerpo) == "Texto hablado real. Mas texto."
    assert mg.palabras(mg.hablado(cuerpo)) == 5


def test_guion_real_pasa_todas_las_reglas(monkeypatch):
    texto = Path("docs/defensa.md").read_text(encoding="utf-8")
    # Extraer la cifra de pruebas citada en el guion para evitar pytest recursivo
    m = next((int(n) for n, tipo in mg.CIFRA.findall(texto) if tipo == "pruebas"), 0)
    monkeypatch.setattr(mg, "pruebas_que_pasan", lambda: m)
    checks = dict((cid, ok) for cid, ok, _ in mg.evaluar_guion(texto))
    assert all(checks.values()), f"Reglas fallidas en docs/defensa.md: {checks}"


def test_demo_coincide_falla_si_falta_un_paso(monkeypatch):
    texto = Path("docs/defensa.md").read_text(encoding="utf-8")
    m = next((int(n) for n, tipo in mg.CIFRA.findall(texto) if tipo == "pruebas"), 0)
    monkeypatch.setattr(mg, "pruebas_que_pasan", lambda: m)
    alterado = texto.replace("- PASO-7 Una falla honesta sin modelo", "")
    checks = dict((cid, ok) for cid, ok, _ in mg.evaluar_guion(alterado))
    assert checks["GUION-8"] is False


def test_pendientes_falla_si_aparece_todo(monkeypatch):
    texto = Path("docs/defensa.md").read_text(encoding="utf-8") + "\nTODO revisar lamina\n"
    m = next((int(n) for n, tipo in mg.CIFRA.findall(texto) if tipo == "pruebas"), 0)
    monkeypatch.setattr(mg, "pruebas_que_pasan", lambda: m)
    checks = dict((cid, ok) for cid, ok, _ in mg.evaluar_guion(texto))
    assert checks["GUION-9"] is False
