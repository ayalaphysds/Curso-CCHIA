"""Verificador de suite de pruebas parciales aisladas (Bloque 39.3)."""

from pathlib import Path
import re
import subprocess
import sys

PLAN = Path("docs/pruebas_parciales.md")

PROHIBIDO = [
    ("red/procesos", re.compile(r"^\s*(?:import|from)\s+(?:httpx|requests|socket|urllib|subprocess)\b")),
    ("docker", re.compile(r"^\s*(?:import|from)\s+docker\b")),
    ("TestClient", re.compile(r"\bTestClient\b")),
    ("servicio.main", re.compile(r"\bservicio\.main\b|from servicio import .*\bmain\b")),
    ("entorno real", re.compile(r"\bos\.environ\b|\bos\.getenv\b|dotenv")),
]


def cargar_filas_plan(ruta: Path = PLAN) -> list[list[str]]:
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
        if celdas[0].lower() == "componente" or all(set(c) <= {"-", ":"} for c in celdas):
            continue
        filas.append(celdas)
    return filas


def main() -> int:
    filas = cargar_filas_plan()
    resultados: list[tuple[str, bool, str]] = []

    # PAR-1: plan_completo
    ok_1 = len(filas) >= 4
    faltantes = []
    for f in filas:
        if any(not f[i] for i in range(5)):
            ok_1 = False
        if not Path(f[4]).is_file():
            ok_1 = False
            faltantes.append(f[4])
    resultados.append(("PAR-1", ok_1, f"{len(filas)} componentes en el plan" if ok_1 else f"plan incompleto o faltan: {faltantes}"))

    # PAR-2: pruebas_suficientes (>=3 tests y >=1 test_contrato)
    insuficientes = []
    for f in filas:
        ruta = Path(f[4])
        if not ruta.is_file():
            continue
        nombres = re.findall(r"(?m)^def (test_\w+)", ruta.read_text(encoding="utf-8"))
        if len(nombres) < 3 or not any(n.startswith("test_contrato") for n in nombres):
            insuficientes.append(f"{f[4]} ({len(nombres)} tests)")
    resultados.append(("PAR-2", bool(filas) and not insuficientes, "todas con >=3 tests y >=1 test_contrato" if not insuficientes else f"insuficientes: {insuficientes}"))

    # PAR-3: pruebas_aisladas
    contaminadas = []
    for f in filas:
        ruta = Path(f[4])
        if not ruta.is_file():
            continue
        for num, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            for etiqueta, patron in PROHIBIDO:
                if patron.search(linea):
                    contaminadas.append(f"{f[4]}:{num} ({etiqueta})")
    resultados.append(("PAR-3", bool(filas) and not contaminadas, "100% aisladas sin red, Docker ni entorno real" if not contaminadas else f"violaciones: {contaminadas}"))

    # PAR-4: pruebas_pasan
    fallidas = []
    for f in filas:
        ruta = Path(f[4])
        if not ruta.is_file():
            fallidas.append(f[4])
            continue
        r = subprocess.run([sys.executable, "-m", "pytest", str(ruta), "-q", "--tb=no"], capture_output=True, text=True)
        if r.returncode != 0:
            fallidas.append(f[4])
    resultados.append(("PAR-4", bool(filas) and not fallidas, f"{len(filas)} archivos pytest OK" if not fallidas else f"fallan: {fallidas}"))

    # PAR-5: defectos_detectados
    sin_def = [f[0] for f in filas if not f[5] or f[6].lower() not in ("si", "sí")]
    resultados.append(("PAR-5", bool(filas) and not sin_def, "todos los defectos registrados y detectados" if not sin_def else f"pendientes: {sin_def}"))

    cumplidas = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
