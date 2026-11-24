"""Verifica las cinco secciones de docs/ficha_diseno_funcional.md y la revision cruzada (Bloque 34.3)."""

from pathlib import Path
import re
import sys

from ficha_datos import cargar_ficha
from verificar_ficha import FICHA, verificar

REVISION = Path("docs/revision_alcance.md")
MIN_HITOS = 3
MAX_HITOS = 6


def verificar_pendientes(ficha: dict) -> list[str]:
    errores: list[str] = []
    for num in ("4", "5"):
        cuerpo = ficha["secciones"][num][1]
        if "[PENDIENTE" in cuerpo or "[COMPLETAR" in cuerpo:
            errores.append(f"Seccion {num} contiene marcadores pendientes o por completar")
    return errores


def verificar_criterios(ficha: dict) -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []
    s4 = ficha["secciones"]["4"][1]

    lineas_ca = re.findall(r"(?m)^- CA.*$", s4)
    patron_ca = re.compile(r"^- (CA-\d{2}) \(([^)]*)\): (.+)$")
    for linea in lineas_ca:
        if not patron_ca.match(linea):
            errores.append(f"Linea de criterio con formato invalido: {linea}")

    criterios = ficha["criterios"]
    if not criterios:
        errores.append("No se encontraron criterios de aceptacion en la seccion 4")
        return errores, avisos

    validos = set(ficha["rf"].keys()) | set(ficha["rnf"].keys())
    cubiertos: set[str] = set()
    for c in criterios:
        if not c["refs"]:
            errores.append(f"{c['id']} no referencia ningun RF o RNF valido")
        for ref in c["refs"]:
            if ref not in validos:
                errores.append(f"{c['id']} referencia un requerimiento inexistente: {ref}")
            else:
                cubiertos.add(ref)
        if not re.search(r'\d|"', c["texto"]):
            avisos.append(f"{c['id']} no tiene ningun dato concreto")

    imprescindibles = set(ficha["alcance"].get("Imprescindible", []))
    esperados = imprescindibles | set(ficha["rnf"].keys())
    for faltante in sorted(esperados - cubiertos):
        errores.append(f"El requerimiento {faltante} no tiene criterio de aceptacion")

    return errores, avisos


def verificar_plan(ficha: dict) -> list[str]:
    errores: list[str] = []
    s5 = ficha["secciones"]["5"][1]

    lineas_h = re.findall(r"(?m)^- H\d+.*$", s5)
    patron_h = re.compile(r"^- (H\d+) \(\d+(?:[.,]\d+)? h\): .+$")
    for linea in lineas_h:
        if not patron_h.match(linea):
            errores.append(f"Linea de hito con formato invalido: {linea}")

    hitos = ficha["hitos"]
    if len(hitos) < MIN_HITOS or len(hitos) > MAX_HITOS:
        errores.append(f"Debe haber entre {MIN_HITOS} y {MAX_HITOS} hitos; encontrados {len(hitos)}")

    disp = ficha["horas_disponibles"]
    marg = ficha["margen_imprevistos"]
    if disp is None:
        errores.append("Falta la linea 'Horas disponibles: <N> h' en la seccion 5")
    if marg is None:
        errores.append("Falta la linea 'Margen de imprevistos: <M> h' en la seccion 5")

    if disp is not None and marg is not None:
        total_h = sum(h["horas"] for h in hitos)
        limite = disp - marg
        if total_h > limite + 1e-9:
            errores.append(
                f"Las horas planificadas ({total_h:.1f} h) superan las disponibles menos margen ({limite:.1f} h)"
            )

    reqs_validos = set(ficha["rf"].keys()) | set(ficha["rnf"].keys())
    cas_validos = {c["id"] for c in ficha["criterios"]}
    cubre_total: set[str] = set()
    cas_total: set[str] = set()

    for h in hitos:
        if not h["cubre"]:
            errores.append(f"{h['id']} no declara que requerimientos cubre ('Cubre:')")
        for ref in h["cubre"]:
            if ref not in reqs_validos:
                errores.append(f"{h['id']} cubre requerimiento inexistente: {ref}")
            else:
                cubre_total.add(ref)
        if not h["criterios"]:
            errores.append(f"{h['id']} no declara con que criterios se comprueba ('Se comprueba con:')")
        for cid in h["criterios"]:
            if cid not in cas_validos:
                errores.append(f"{h['id']} cita criterio inexistente: {cid}")
            else:
                cas_total.add(cid)

    for rf in sorted(set(ficha["alcance"].get("Imprescindible", [])) - cubre_total):
        errores.append(f"El RF imprescindible {rf} no esta cubierto por ningun hito")
    for cid in sorted(cas_validos - cas_total):
        errores.append(f"El criterio {cid} no es comprobado por ningun hito")

    return errores


def verificar_revision(ruta: Path = REVISION) -> list[str]:
    errores: list[str] = []
    if not ruta.is_file():
        return [f"No existe {ruta}"]
    texto = ruta.read_text(encoding="utf-8")
    hallazgos = re.findall(r"(?m)^- Hallazgo \d+(?: \([^)]*\))?: .+$", texto)
    decisiones = re.findall(r"(?m)^  Decisión: (?:aceptado|rechazado|aplazado)\b", texto)
    if len(hallazgos) < 2:
        errores.append(f"Se requieren al menos 2 hallazgos en {ruta}; encontrados {len(hallazgos)}")
    if len(decisiones) != len(hallazgos):
        errores.append(
            f"Cada hallazgo debe tener su linea '  Decisión: ...' ({len(decisiones)} decisiones para {len(hallazgos)} hallazgos)"
        )
    return errores


def main() -> int:
    errores_1_3, avisos_1_3 = verificar(FICHA)
    for av in avisos_1_3:
        print(f"AVISO: {av}")
    if errores_1_3:
        for err in errores_1_3:
            print(f"ERROR: {err}")
        return 1

    ficha = cargar_ficha(FICHA)
    errores_pend = verificar_pendientes(ficha)
    if errores_pend:
        for err in errores_pend:
            print(f"ERROR: {err}")
        return 1

    errores_ca, avisos_ca = verificar_criterios(ficha)
    for av in avisos_ca:
        print(f"AVISO: {av}")
    errores_plan = verificar_plan(ficha)
    if errores_ca or errores_plan:
        for err in errores_ca + errores_plan:
            print(f"ERROR: {err}")
        return 1

    errores_rev = verificar_revision(REVISION)
    if errores_rev:
        for err in errores_rev:
            print(f"ERROR: {err}")
        return 1

    print("Ficha verificada: las cinco secciones son coherentes")
    print("5 de 5 comprobaciones cumplidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
