"""Verificador cruzado de 7 reglas sobre decisiones, limitaciones, riesgos y README (Bloque 45.3 CORE)."""

from pathlib import Path
import re
import sys

from alucinaciones import SONDAS
from ataques import ATAQUES
import ejecutar_matriz as em
import riesgos as mod_riesgos
import transferencia as tr

DOC_DEC = Path("docs/decisiones.md")
DOC_LIM = Path("docs/limitaciones.md")
DOC_README = Path("README.md")

CAMPOS = ("Estado", "Contexto", "Decisión", "Alternativas descartadas", "Costo")
MINIMO_DECISIONES = 5
MIN_TEXTO = 30
ID_D = re.compile(r"\bD-\d{2}\b")
ID_L = re.compile(r"LIM-\d{2}")


def cargar_decisiones(ruta: Path = DOC_DEC) -> list[dict]:
    if not ruta.is_file():
        return []
    texto = ruta.read_text(encoding="utf-8")
    encabezados = list(re.finditer(r"(?m)^## (D-\d{2}) .*$", texto))
    salida = []
    for i, m in enumerate(encabezados):
        did = m.group(1)
        inicio = m.end()
        fin = encabezados[i + 1].start() if i + 1 < len(encabezados) else len(texto)
        bloque = texto[inicio:fin]
        campos: dict[str, str] = {}
        clave_actual: str | None = None
        for linea in bloque.splitlines():
            mc = re.match(r"^- \*\*(.+?):\*\* ?(.*)", linea)
            if mc:
                clave_actual = mc.group(1).strip()
                campos[clave_actual] = mc.group(2).strip()
            elif clave_actual and linea.startswith("  "):
                campos[clave_actual] = (campos[clave_actual] + " " + linea.strip()).strip()
        salida.append({"id": did, "campos": campos})
    return salida


def cargar_limitaciones(ruta: Path = DOC_LIM) -> list[dict]:
    if not ruta.is_file():
        return []
    filas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        limpia = linea.strip()
        if not limpia.startswith("|") or not limpia.endswith("|"):
            continue
        celdas = [c.strip() for c in limpia.strip("|").split("|")]
        if len(celdas) == 6 and re.fullmatch(r"LIM-\d{2}", celdas[0]):
            filas.append(
                {
                    "id": celdas[0],
                    "que": celdas[1],
                    "origen": celdas[2],
                    "riesgo": celdas[3],
                    "efecto": celdas[4],
                    "decision": celdas[5],
                }
            )
    return filas


def declaradas() -> set[str]:
    origenes: set[str] = set()
    for a in ATAQUES:
        if a.get("hallazgo", {}).get("clasificacion") == "limitacion":
            origenes.add(f"ataques:{a['id']}")
    for s in SONDAS:
        if "decision" in s:
            origenes.add(f"alucinaciones:{s['id']}")
    for nombre in ("matriz_modelo", "matriz_pruebas"):
        for e in em.cargar(nombre):
            if e.get("hallazgo", {}).get("clasificacion") == "limitacion":
                origenes.add(f"{nombre}:{e['id']}")
    for o in tr.OBSERVACIONES:
        if o.get("causa") == "producto":
            origenes.add(f"transferencia:{o['id']}")
    return origenes


def main() -> int:
    decs = cargar_decisiones()
    lims = cargar_limitaciones()
    readme_txt = DOC_README.read_text(encoding="utf-8") if DOC_README.is_file() else ""
    riesgos_por_id = {r["id"]: r for r in mod_riesgos.RIESGOS}
    checks: list[tuple[str, bool, str]] = []

    # DEC-1: decisiones_completas
    incompletas = []
    for d in decs:
        c = d["campos"]
        if any(not c.get(k) for k in CAMPOS) or c.get("Estado") not in ("vigente", "reemplazada"):
            incompletas.append(d["id"])
    ok_1 = len(decs) >= MINIMO_DECISIONES and not incompletas
    checks.append(("DEC-1", ok_1, f"{len(decs)} decisiones completas" if ok_1 else f"incompletas={incompletas}, total={len(decs)}"))

    # DEC-2: costos_reales
    cortas = [
        d["id"] for d in decs
        if len(d["campos"].get("Alternativas descartadas", "")) < MIN_TEXTO
        or len(d["campos"].get("Costo", "")) < MIN_TEXTO
    ]
    checks.append(("DEC-2", bool(decs) and not cortas, "alternativas y costos fundamentados (>=30 chars)" if not cortas else f"muy breves: {cortas}"))

    # DEC-3: readme_cita
    vigentes = {d["id"] for d in decs if d["campos"].get("Estado") == "vigente"}
    todos_d = {d["id"] for d in decs}
    citados_d = set(ID_D.findall(readme_txt))
    faltan_d = sorted(vigentes - citados_d)
    fantasma_d = sorted(citados_d - todos_d)
    cita_docs = "docs/decisiones.md" in readme_txt and "docs/limitaciones.md" in readme_txt
    ok_3 = bool(vigentes) and not faltan_d and not fantasma_d and cita_docs
    checks.append(("DEC-3", ok_3, f"README cita {len(vigentes)} decisiones vigentes y ambos docs" if ok_3 else f"faltan={faltan_d}, fantasma={fantasma_d}, cita_docs={cita_docs}"))

    # DEC-4: limitaciones_completas (igualdad bidireccional)
    origenes_doc = {
        parte.strip()
        for f in lims
        for parte in f["origen"].split(",")
        if parte.strip()
    }
    origenes_cod = declaradas()
    ok_4 = origenes_doc == origenes_cod
    checks.append(("DEC-4", ok_4, f"coincidencia exacta de {len(origenes_cod)} origenes declarados" if ok_4 else f"doc-cod={sorted(origenes_doc - origenes_cod)}, cod-doc={sorted(origenes_cod - origenes_doc)}"))

    # DEC-5: limitaciones_utiles
    malas_lim = []
    for f in lims:
        if len(f["efecto"]) < MIN_TEXTO or len(f["decision"]) < MIN_TEXTO:
            malas_lim.append(f"{f['id']}(texto)")
            continue
        r = riesgos_por_id.get(f["riesgo"])
        if not r or r["estado"] not in ("parcial", "aceptada"):
            malas_lim.append(f"{f['id']}(riesgo {f['riesgo']})")
            continue
        for ori in [p.strip() for p in f["origen"].split(",") if p.strip()]:
            cod_item = ori.split(":", 1)[1].strip() if ":" in ori else ori
            if cod_item not in r.get("limites", []):
                malas_lim.append(f"{f['id']}({cod_item} no en {r['id']}.limites)")
    checks.append(("DEC-5", bool(lims) and not malas_lim, f"{len(lims)} limitaciones enlazadas a riesgos parciales/aceptados" if not malas_lim else f"errores: {malas_lim}"))

    # DEC-6: readme_limitaciones
    ids_lim = {f["id"] for f in lims}
    citados_l = set(ID_L.findall(readme_txt))
    faltan_l = sorted(ids_lim - citados_l)
    ok_6 = bool(ids_lim) and not faltan_l
    checks.append(("DEC-6", ok_6, f"README cita las {len(ids_lim)} limitaciones" if ok_6 else f"faltan en README: {faltan_l}"))

    # DEC-7: transferencia_registrada
    lims_por_id = {f["id"]: f for f in lims}
    faltan_t = []
    for o in tr.OBSERVACIONES:
        if o.get("causa") == "producto":
            ref = o.get("ref")
            fila = lims_por_id.get(ref)
            if not fila or f"transferencia:{o['id']}" not in fila["origen"]:
                faltan_t.append(f"{o['id']}->{ref}")
    checks.append(("DEC-7", not faltan_t, "observaciones de producto de transferencia trazadas" if not faltan_t else f"faltan: {faltan_t}"))

    cumplidas = sum(1 for _, ok, _ in checks if ok)
    for rid, ok, det in checks:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
