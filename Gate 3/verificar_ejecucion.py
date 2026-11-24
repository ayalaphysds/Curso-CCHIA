"""Verifica escenarios E2E, bitacora de ajustes, repetibilidad y coherencia (Bloque 40.3)."""

from pathlib import Path
import re
import sys
import httpx

import ejecutar_escenarios as ee
from escenarios import ESCENARIOS

BITACORA = Path("docs/bitacora_ajustes.md")
OBLIGATORIAS = {"fuera de alcance", "error esperado", "control"}
CIFRA = re.compile(r"(\d+) de (\d+)")


def cargar_bitacora(ruta: Path = BITACORA) -> list[list[str]]:
    if not ruta.is_file():
        return []
    filas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        limpia = linea.strip()
        if not limpia.startswith("|") or not limpia.endswith("|"):
            continue
        celdas = [c.strip() for c in limpia.strip("|").split("|")]
        if len(celdas) != 7:
            continue
        if celdas[0].lower().startswith("iteraci") or all(set(c) <= {"-", ":"} for c in celdas):
            continue
        filas.append(celdas)
    return filas


def main() -> int:
    resultados: list[tuple[str, bool, str]] = []

    # EJE-1: escenarios_completos
    ids = [e["id"] for e in ESCENARIOS]
    cats = {e["categoria"] for e in ESCENARIOS}
    ok_1 = len(ESCENARIOS) >= 10 and len(ids) == len(set(ids)) and len(cats) >= 4 and OBLIGATORIAS <= cats
    resultados.append(("EJE-1", ok_1, f"{len(ESCENARIOS)} escenarios, {len(cats)} categorias"))

    # EJE-2: bitacora_completa
    filas = cargar_bitacora()
    ok_2 = len(filas) >= 2
    mejora = False
    ultimo_conservar: tuple[int, int] | None = None
    for f in filas:
        if any(not c for c in f):
            ok_2 = False
        m_a = CIFRA.search(f[4])
        m_d = CIFRA.search(f[5])
        dec = f[6].lower()
        if not m_a or not m_d or dec not in ("conservar", "descartar"):
            ok_2 = False
        elif dec == "conservar":
            ultimo_conservar = (int(m_d.group(1)), int(m_d.group(2)))
            if int(m_d.group(1)) > int(m_a.group(1)):
                mejora = True
    ok_2 = ok_2 and mejora
    resultados.append(("EJE-2", ok_2, f"{len(filas)} iteraciones en bitacora, ultimo conservar={ultimo_conservar}"))

    # EJE-3: solucion_responde
    caidos = []
    for nombre, base in ee.DESTINOS.items():
        try:
            r = httpx.get(base.rstrip("/") + "/salud", timeout=5.0)
            if r.status_code != 200:
                caidos.append(f"{nombre}({r.status_code})")
        except httpx.HTTPError:
            caidos.append(f"{nombre}(sin conexion)")
    ok_3 = len(caidos) == 0
    resultados.append(("EJE-3", ok_3, "API e Interfaz responden 200 en /salud" if ok_3 else f"no responden: {caidos}"))

    if ok_3:
        primera = ee.correr()
        cumplidos = sum(1 for r in primera if not r["motivos"])
        ok_4 = cumplidos == len(primera)
        resultados.append(("EJE-4", ok_4, f"{cumplidos} de {len(primera)} escenarios cumplidos"))

        segunda = ee.correr()
        iguales = ee.firma(primera) == ee.firma(segunda)
        coherente = ultimo_conservar == (cumplidos, len(primera))
        ok_5 = iguales and coherente
        resultados.append(("EJE-5", ok_5, f"repetible={iguales}, coherente_bitacora={coherente}"))

    cumplidas = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de 5 comprobaciones cumplidas")
    return 0 if cumplidas == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
