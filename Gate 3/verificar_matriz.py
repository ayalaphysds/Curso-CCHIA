"""Verificador de 6 reglas sobre matriz_pruebas.py y docs/matriz_pruebas.md (Bloque 42.3)."""

from pathlib import Path
import re
import sys

import ejecutar_matriz as em

FICHA = Path("docs/ficha_diseno_funcional.md")
DOC_MATRIZ = Path("docs/matriz_pruebas.md")
CAMPOS = ("id", "tipo", "escenario", "peticion", "esperado", "cubre")
TIPOS_VALIDOS = {"valido", "invalido", "borde"}
CLASIFICACIONES = {"defecto", "prueba", "limitacion", "entorno"}
MIN_DECISION = 20


def main() -> int:
    nombre = "matriz_pruebas"
    if "--matriz" in sys.argv:
        idx = sys.argv.index("--matriz")
        if idx + 1 < len(sys.argv):
            nombre = sys.argv[idx + 1]

    matriz = em.cargar(nombre)
    resultados_exec = em.ejecutar(matriz)
    checks: list[tuple[str, bool, str]] = []

    # MAT-1: estructura
    ids = [e.get("id") for e in matriz]
    tipos = {e.get("tipo") for e in matriz}
    ok_1 = (
        len(matriz) >= 4
        and all(all(k in e for k in CAMPOS) for e in matriz)
        and len(ids) == len(set(ids))
        and tipos <= TIPOS_VALIDOS
        and tipos == TIPOS_VALIDOS
    )
    checks.append(("MAT-1", ok_1, f"{len(matriz)} escenarios, tipos={sorted(tipos)}"))

    # MAT-2: esperado_verificable
    mal_esp = [
        e["id"] for e in matriz
        if "estado" not in e["esperado"] or not (e["esperado"].get("contiene") or "fuentes" in e["esperado"])
    ]
    checks.append(("MAT-2", len(mal_esp) == 0, "todos los esperados son verificables" if not mal_esp else f"incompletos: {mal_esp}"))

    # MAT-3: trazabilidad con docs/ficha_diseno_funcional.md
    if not FICHA.is_file():
        checks.append(("MAT-3", False, f"no existe {FICHA}"))
    else:
        txt_ficha = FICHA.read_text(encoding="utf-8")
        codigos_ficha = set(re.findall(r"\b(?:RF|RNF|CA)-\d{2}\b", txt_ficha))
        m_imp = re.search(r"(?m)^Imprescindible: (.*)$", txt_ficha)
        imprescindibles = set(re.findall(r"RF-\d{2}", m_imp.group(1))) if m_imp else set()
        cubiertos = {c for e in matriz for c in e.get("cubre", [])}
        inexistentes = sorted(cubiertos - codigos_ficha)
        sin_cubrir = sorted(imprescindibles - cubiertos)
        vacios = [e["id"] for e in matriz if not e.get("cubre")]
        ok_3 = not inexistentes and not sin_cubrir and not vacios
        checks.append(("MAT-3", ok_3, f"trazabilidad completa ({len(imprescindibles)} imprescindibles cubiertos)" if ok_3 else f"inexistentes={inexistentes}, sin_cubrir={sin_cubrir}"))

    # MAT-4: registro_vigente
    if not DOC_MATRIZ.is_file():
        checks.append(("MAT-4", False, f"no existe {DOC_MATRIZ}"))
    else:
        m_h = re.search(r"Huella de la matriz: ([0-9a-f]{12})", DOC_MATRIZ.read_text(encoding="utf-8"))
        esperada = em.huella(matriz)
        ok_4 = bool(m_h) and m_h.group(1) == esperada
        checks.append(("MAT-4", ok_4, f"huella vigente {esperada}" if ok_4 else f"huella desactualizada ({m_h.group(1) if m_h else None} != {esperada})"))

    # MAT-5: clasificadas
    sin_explicar = []
    for r in resultados_exec:
        if r["resultado"] != "PASA":
            h = r.get("hallazgo") or {}
            if h.get("clasificacion") != "limitacion" or len(str(h.get("decision", ""))) < MIN_DECISION:
                sin_explicar.append(r["id"])
    checks.append(("MAT-5", len(sin_explicar) == 0, "0 fallas sin clasificar" if not sin_explicar else f"sin clasificar: {sin_explicar}"))

    # MAT-6: sin_errores_5xx
    errores_5xx = [r["id"] for r in resultados_exec if r["estado"] >= 500]
    checks.append(("MAT-6", len(errores_5xx) == 0, "0 errores 5xx" if not errores_5xx else f"5xx en: {errores_5xx}"))

    cumplidas = sum(1 for _, ok, _ in checks if ok)
    for rid, ok, det in checks:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
