"""Verificador cruzado de 8 reglas sobre README.md (Bloque 44.3)."""

from pathlib import Path
import re
import subprocess
import sys

import buscar_secretos
import contar_friccion as cf

README = Path("README.md")
DOCKERFILE = Path("Dockerfile")
COMPOSE = Path("compose.yaml")
ENV_EXAMPLE = Path(".env.example")

MODULOS = {"pytest", "venv", "uvicorn"}
PERMITIDAS = {".env", ".venv"}
EXTENSIONES = (".py", ".md", ".yaml", ".yml", ".txt", ".png", ".json", ".jsonl")


def sin_secretos(texto: str) -> tuple[bool, str]:
    if buscar_secretos.CLAVE_GOOGLE.search(texto) or buscar_secretos.ASIGNACION.search(texto):
        return False, "se detecto un posible secreto en el texto"
    return True, "sin secretos detectados"


def _variables_en_servicio() -> set[str]:
    encontradas: set[str] = set()
    for ruta in Path("servicio").glob("*.py"):
        encontradas.update(re.findall(r'environ\.get\("([A-Z0-9_]+)"', ruta.read_text(encoding="utf-8")))
    return encontradas


def verificar_readme(texto: str | None = None, ejecutar_pytest: bool = True) -> list[tuple[str, bool, str]]:
    if texto is None:
        if not README.is_file():
            return [("README-1", False, f"no existe {README}")]
        texto = README.read_text(encoding="utf-8")

    checks: list[tuple[str, bool, str]] = []

    # README-1: secciones_presentes
    faltan_sec = cf.faltantes_en_readme(texto)
    checks.append(("README-1", not faltan_sec, "10 secciones del diario presentes" if not faltan_sec else f"faltan: {faltan_sec}"))

    # README-2: variables (.env.example == servicio/*.py == seccion configuracion, etiquetadas secreto/configuracion)
    vars_env = set(re.findall(r"(?m)^([A-Z][A-Z0-9_]+)=", ENV_EXAMPLE.read_text(encoding="utf-8"))) if ENV_EXAMPLE.is_file() else set()
    vars_srv = _variables_en_servicio()
    secs = cf.secciones(texto)
    cuerpo_cfg = next((v for k, v in secs.items() if "configuracion" in k), "")
    vars_doc = set(re.findall(r"`([A-Z][A-Z0-9_]{2,})`", cuerpo_cfg))
    sin_etiqueta = []
    for var in sorted(vars_doc):
        lineas_var = [ln for ln in cuerpo_cfg.splitlines() if f"`{var}`" in ln]
        if not any(re.search(r"\((secreto|configuracion)\)", cf.normal(ln)) for ln in lineas_var):
            sin_etiqueta.append(var)
    ok_2 = bool(vars_env) and vars_env == vars_srv == vars_doc and not sin_etiqueta
    det_2 = f"{len(vars_env)} variables sincronizadas y etiquetadas" if ok_2 else f"env={sorted(vars_env)} srv={sorted(vars_srv)} doc={sorted(vars_doc)} sin_et={sin_etiqueta}"
    checks.append(("README-2", ok_2, det_2))

    # README-3: comandos_validos
    bloques = re.findall(r"```(?:[a-zA-Z0-9_-]*)\n(.*?)```", texto, flags=re.S)
    candidatos = [ln.strip() for b in bloques for ln in b.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    candidatos += re.findall(r"`([^`\n]+)`", re.sub(r"```.*?```", "", texto, flags=re.S))
    vistos = 0
    rotos = []
    for cmd in candidatos:
        m_mod = re.match(r"^python3?\s+-m\s+([A-Za-z0-9_]+)\b", cmd)
        if m_mod:
            vistos += 1
            if m_mod.group(1) not in MODULOS:
                rotos.append(cmd)
            continue
        m_py = re.match(r"^python3?\s+([^\s]+\.py)\b", cmd)
        if m_py:
            vistos += 1
            if not Path(m_py.group(1)).is_file():
                rotos.append(cmd)
            continue
        m_cp = re.match(r"^cp\s+([^\s]+)\s+([^\s]+)", cmd)
        if m_cp:
            vistos += 1
            if not Path(m_cp.group(1)).is_file():
                rotos.append(cmd)
            continue
        m_pip = re.match(r"^pip\s+install\s+-r\s+([^\s]+)", cmd)
        if m_pip:
            vistos += 1
            if not Path(m_pip.group(1)).is_file():
                rotos.append(cmd)
    ok_3 = vistos > 0 and not rotos
    checks.append(("README-3", ok_3, f"{vistos} comandos validados" if ok_3 else f"vistos={vistos}, rotos={rotos}"))

    # README-4: rutas_validas
    sin_bloques = re.sub(r"```.*?```", "", texto, flags=re.S)
    rutas_inline = re.findall(r"`([^`\s]+)`", sin_bloques)
    vistas: set[str] = set()
    inexistentes: list[str] = []
    for r in rutas_inline:
        limpio = r.rstrip(".,;:")
        if (
            limpio.startswith(("/", "http://", "https://", "-", "--"))
            or limpio in PERMITIDAS
            or any(ch in limpio for ch in "{}*<>=")
        ):
            continue
        if "/" in limpio or limpio.endswith(EXTENSIONES):
            vistas.add(limpio)
            if not Path(limpio).exists():
                inexistentes.append(limpio)
    ok_4 = bool(vistas) and not inexistentes
    checks.append(("README-4", ok_4, f"{len(vistas)} rutas existentes" if ok_4 else f"inexistentes={sorted(set(inexistentes))}"))

    # README-5: puertos
    puertos_cmp = set(re.findall(r'"(\d+):\d+"', COMPOSE.read_text(encoding="utf-8"))) if COMPOSE.is_file() else set()
    puertos_doc = set(re.findall(r"127\.0\.0\.1:(\d+)", texto))
    ok_5 = bool(puertos_cmp) and puertos_cmp == puertos_doc
    checks.append(("README-5", ok_5, f"puertos {sorted(puertos_cmp)} coinciden" if ok_5 else f"compose={sorted(puertos_cmp)} readme={sorted(puertos_doc)}"))

    # README-6: sin_secretos
    ok_6, det_6 = sin_secretos(texto)
    checks.append(("README-6", ok_6, det_6))

    # README-7: version_de_python
    m_df = re.search(r"FROM\s+python:(\d+\.\d+)", DOCKERFILE.read_text(encoding="utf-8")) if DOCKERFILE.is_file() else None
    ver_df = m_df.group(1) if m_df else None
    vers_readme = set(re.findall(r"Python\s+(\d+\.\d+)", texto))
    ok_7 = ver_df is not None and ver_df in vers_readme
    checks.append(("README-7", ok_7, f"Python {ver_df} consistente con Dockerfile" if ok_7 else f"dockerfile={ver_df}, readme={sorted(vers_readme)}"))

    # README-8: pruebas_ejecutan
    tiene_cmd = "python -m pytest -q" in texto
    if ejecutar_pytest and tiene_cmd:
        r_p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x"], capture_output=True, text=True)
        ok_8 = r_p.returncode == 0
        det_8 = "pytest paso sin fallas" if ok_8 else "pytest fallo"
    else:
        ok_8 = tiene_cmd
        det_8 = "comando pytest presente" if tiene_cmd else "falta 'python -m pytest -q'"
    checks.append(("README-8", ok_8, det_8))

    return checks


def main() -> int:
    checks = verificar_readme()
    cumplidas = sum(1 for _, ok, _ in checks if ok)
    for rid, ok, det in checks:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
