"""Medidor de 9 reglas sobre el guion de defensa tecnica docs/defensa.md (Bloques S2.2 y S2.3)."""

from pathlib import Path
import re
import subprocess
import sys

from ataques import ATAQUES
from contar_friccion import normal
from ejemplos_api import EJEMPLOS
import riesgos as mod_riesgos
import transferencia as tr
import verificar_readme as vr

GUION = Path("docs/defensa.md")
MINUTOS_TOTALES = 8
PALABRAS_POR_MINUTO = 130
MAX_DIAPOSITIVAS = 8
CLAVES = ("problema", "arquitectura", "riesgos", "demo", "cierre")

IDENTIFICADOR = re.compile(r"\b(R|D|LIM|T|A)-(\d{2})\b")
CIFRA = re.compile(r"\b(\d+)\s+(pruebas|riesgos|decisiones|limitaciones|ejemplos)\b")
PENDIENTE = re.compile(r"\[COMPLETAR\]|\bTODO\b", re.I)
TECNOLOGIAS = (
    "FastAPI",
    "Docker",
    "Gemini",
    "Chroma",
    "LangGraph",
    "Redis",
    "PostgreSQL",
    "Kubernetes",
    "uvicorn",
    "pydantic",
)
SUFIJOS = {".py", ".txt", ".yaml", ".yml", ""}
IGNORAR = {".git", ".venv", "__pycache__", ".pytest_cache", "tests"}


def secciones_con_tiempo(texto: str) -> list[tuple[str, int, str]]:
    patron = re.compile(r"^## \d+\. ([^\n(]+?) \((\d+) min\)\n(.*?)(?=^## |\Z)", re.M | re.S)
    salida = []
    for m in patron.finditer(texto):
        clave = normal(m.group(1)).split()[0]
        salida.append((clave, int(m.group(2)), m.group(3).strip()))
    return salida


def hablado(cuerpo: str) -> str:
    lineas = []
    dentro_bloque = False
    for ln in cuerpo.splitlines():
        s = ln.strip()
        if s.startswith("```"):
            dentro_bloque = not dentro_bloque
            continue
        if dentro_bloque or not s:
            continue
        if s.startswith(("|", "- ", "#")):
            continue
        lineas.append(s)
    return " ".join(lineas)


def palabras(texto: str) -> int:
    return len(re.findall(r"\S+", texto))


def ids_existentes() -> dict[str, set[str]]:
    dec_txt = Path("docs/decisiones.md").read_text(encoding="utf-8") if Path("docs/decisiones.md").is_file() else ""
    lim_txt = Path("docs/limitaciones.md").read_text(encoding="utf-8") if Path("docs/limitaciones.md").is_file() else ""
    return {
        "R": {r["id"] for r in mod_riesgos.RIESGOS},
        "D": set(re.findall(r"(?m)^## (D-\d{2})", dec_txt)),
        "LIM": set(re.findall(r"(?m)^\| (LIM-\d{2}) ", lim_txt)),
        "T": {o["id"] for o in tr.OBSERVACIONES},
        "A": {a["id"] for a in ATAQUES},
    }


def pruebas_que_pasan() -> int:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True)
    salida = r.stdout + "\n" + r.stderr
    return sum(int(x) for x in re.findall(r"(\d+) passed", salida))


def _texto_codigo(raiz: Path = Path(".")) -> str:
    trozos = []
    for ruta in raiz.rglob("*"):
        if any(p in IGNORAR for p in ruta.parts):
            continue
        if not ruta.is_file() or ruta.name == "medir_guion.py":
            continue
        if ruta.suffix.lower() in SUFIJOS and ruta.suffix.lower() != ".md":
            trozos.append(ruta.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(trozos).lower()


def evaluar_guion(texto: str) -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []
    secs = secciones_con_tiempo(texto)
    por_clave = {k: (mins, cuerpo) for k, mins, cuerpo in secs}

    # GUION-1: secciones y tiempo
    claves_obs = tuple(k for k, _, _ in secs)
    total_min = sum(m for _, m, _ in secs)
    ok_1 = claves_obs == CLAVES and total_min == MINUTOS_TOTALES
    checks.append(("GUION-1", ok_1, f"secciones={claves_obs}, tiempo={total_min} min"))

    # GUION-2: palabras por seccion hablada
    excesos = []
    habladas = 0
    for clave, mins, cuerpo in secs:
        if clave == "demo":
            continue
        habladas += 1
        n = palabras(hablado(cuerpo))
        tope = mins * PALABRAS_POR_MINUTO
        if n == 0 or n > tope:
            excesos.append(f"{clave}({n}/{tope})")
    ok_2 = habladas > 0 and not excesos
    checks.append(("GUION-2", ok_2, "todas las secciones caben en 130 pal/min" if ok_2 else f"fuera de tope: {excesos}"))

    # GUION-3: identificadores existentes y cobertura minima
    exist = ids_existentes()
    inexistentes = []
    for pref, num in IDENTIFICADOR.findall(texto):
        cid = f"{pref}-{num}"
        if cid not in exist.get(pref, set()):
            inexistentes.append(cid)
    cuerpo_arq = por_clave.get("arquitectura", (0, ""))[1]
    cuerpo_rie = por_clave.get("riesgos", (0, ""))[1]
    tiene_d = bool(re.search(r"\bD-\d{2}\b", cuerpo_arq))
    tiene_r = bool(re.search(r"\bR-\d{2}\b", cuerpo_rie))
    tiene_lim = bool(re.search(r"\bLIM-\d{2}\b", cuerpo_rie))
    ok_3 = not inexistentes and tiene_d and tiene_r and tiene_lim
    checks.append(("GUION-3", ok_3, "identificadores validos y trazados" if ok_3 else f"inexistentes={inexistentes}, D={tiene_d}, R={tiene_r}, LIM={tiene_lim}"))

    # GUION-4: riesgos mayores citados en riesgos
    max_res = max(mod_riesgos.residual(r) for r in mod_riesgos.RIESGOS)
    mayores = [r["id"] for r in mod_riesgos.RIESGOS if mod_riesgos.residual(r) == max_res]
    faltan_may = [rid for rid in mayores if rid not in cuerpo_rie]
    checks.append(("GUION-4", not faltan_may, f"riesgos de mayor residual ({mayores}) citados" if not faltan_may else f"faltan: {faltan_may}"))

    # GUION-5: cifras reales del proyecto
    reales = {
        "riesgos": len(mod_riesgos.RIESGOS),
        "decisiones": len(exist["D"]),
        "limitaciones": len(exist["LIM"]),
        "ejemplos": len(EJEMPLOS),
        "pruebas": pruebas_que_pasan(),
    }
    citadas = CIFRA.findall(texto)
    malas_cif = []
    for num_str, tipo in citadas:
        if int(num_str) != reales[tipo]:
            malas_cif.append(f"{num_str} {tipo} (real={reales[tipo]})")
    ok_5 = bool(citadas) and not malas_cif
    checks.append(("GUION-5", ok_5, f"{len(citadas)} cifras coinciden con el repositorio" if ok_5 else f"errores={malas_cif}, citadas={len(citadas)}"))

    # GUION-6: tecnologias presentes en codigo/config
    codigo = _texto_codigo()
    mencionadas = [t for t in TECNOLOGIAS if re.search(rf"\b{re.escape(t)}\b", texto, re.I)]
    fantasmas = [t for t in mencionadas if t.lower() not in codigo]
    ok_6 = bool(mencionadas) and not fantasmas
    checks.append(("GUION-6", ok_6, f"tecnologias verificadas: {mencionadas}" if ok_6 else f"mencionadas={mencionadas}, sin codigo={fantasmas}"))

    # GUION-7: diapositivas
    m_diap = re.search(r"(?ms)^## Diapositivas\n(.*?)(?=^## |\Z)", texto)
    if not m_diap:
        checks.append(("GUION-7", False, "falta seccion '## Diapositivas'"))
    else:
        filas = re.findall(r"(?m)^\| (\d+) \| ([^|]+?) \| ([^|]+?) \|$", m_diap.group(1))
        secciones_cubiertas = {normal(sec).split()[0] for _, sec, _ in filas}
        ok_7 = 1 <= len(filas) <= MAX_DIAPOSITIVAS and set(CLAVES) <= secciones_cubiertas
        checks.append(("GUION-7", ok_7, f"{len(filas)} diapositivas cubren las 5 secciones" if ok_7 else f"filas={len(filas)}, cubiertas={sorted(secciones_cubiertas)}"))

    # GUION-8: demo coincide con ensayo_demo.PASOS
    import ensayo_demo

    cuerpo_demo = por_clave.get("demo", (0, ""))[1]
    pasos_guion = re.findall(r"(?m)^- (PASO-\d+) (.+)$", cuerpo_demo)
    pasos_demo = [(p["id"], p["titulo"]) for p in ensayo_demo.PASOS]
    ok_8 = (
        bool(pasos_guion)
        and len(pasos_guion) == len(pasos_demo)
        and all(
            ig == id_ and normal(tg) == normal(td)
            for (ig, tg), (id_, td) in zip(pasos_guion, pasos_demo)
        )
    )
    checks.append(("GUION-8", ok_8, f"{len(pasos_guion)} pasos coinciden con ensayo_demo.py" if ok_8 else "desfase entre demo del guion y ensayo_demo.PASOS"))

    # GUION-9: sin pendientes ni secretos
    sin_pend = not PENDIENTE.search(texto)
    ok_sec, det_sec = vr.sin_secretos(texto)
    ok_9 = sin_pend and ok_sec
    checks.append(("GUION-9", ok_9, "sin marcadores pendientes ni secretos" if ok_9 else f"pendientes={not sin_pend}, {det_sec}"))

    return checks


def main() -> int:
    if not GUION.is_file():
        print(f"FALLA GUION-0: no existe {GUION}")
        print("0 de 9 comprobaciones cumplidas")
        return 1
    checks = evaluar_guion(GUION.read_text(encoding="utf-8"))
    cumplidas = sum(1 for _, ok, _ in checks if ok)
    for rid, ok, det in checks:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
