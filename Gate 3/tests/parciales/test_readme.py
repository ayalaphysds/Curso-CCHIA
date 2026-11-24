"""Pruebas unitarias de verificar_readme.py (Bloque 44.3)."""

import verificar_readme as vr


def test_sin_secretos_aprueba_texto_limpio():
    ok, _ = vr.sin_secretos("GEMINI_API_KEY=\nENTORNO=desarrollo")
    assert ok is True


def test_sin_secretos_detecta_clave_google():
    falsa = "AIza" + "A" * 35
    ok, _ = vr.sin_secretos(f"clave={falsa}")
    assert ok is False


def test_sin_secretos_detecta_asignacion_secreto():
    ok, _ = vr.sin_secretos("GEMINI_API_KEY=clave_secreta_no_permitida_12345")
    assert ok is False


def test_readme_vacio_falla_secciones():
    checks = dict((cid, ok) for cid, ok, _ in vr.verificar_readme("# Vacio\n", ejecutar_pytest=False))
    assert checks["README-1"] is False
    assert checks["README-5"] is False


def test_readme_con_ruta_inexistente_falla_readme_4():
    checks = dict(
        (cid, ok)
        for cid, ok, _ in vr.verificar_readme("Ver `no_existe_archivo.py`.", ejecutar_pytest=False)
    )
    assert checks["README-4"] is False


def test_readme_sin_comando_pytest_falla_readme_8():
    checks = dict(
        (cid, ok)
        for cid, ok, _ in vr.verificar_readme("## Pruebas\nSin comando.\n", ejecutar_pytest=False)
    )
    assert checks["README-8"] is False


def test_readme_real_pasa_reglas_estaticas():
    checks = vr.verificar_readme(ejecutar_pytest=False)
    fallas = [cid for cid, ok, _ in checks if not ok]
    assert not fallas, f"Reglas fallidas en README.md: {fallas}"
