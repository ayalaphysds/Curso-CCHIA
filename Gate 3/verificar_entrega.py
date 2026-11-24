"""Verifica entrega de composicion, README, secretos y verificacion cruzada (Bloque 38.3)."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import yaml

SECCIONES_README = [
    "Requisitos",
    "Configuración",
    "Cómo arrancar",
    "Cómo comprobar que funciona",
    "Cómo detener",
    "Problemas frecuentes",
]

EXTENSIONES_ARCHIVO = (".py", ".md", ".yaml", ".yml", ".txt", ".png", ".json", ".jsonl")
PERMITIDAS_NO_VERSIONADAS = {".env", ".venv"}


def _cargar_compose() -> tuple[dict | None, str]:
    compose_path = Path("compose.yaml")
    if not compose_path.is_file():
        return None, "no existe compose.yaml"

    if shutil.which("docker"):
        r = subprocess.run(["docker", "compose", "config", "--format", "json"], capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout), "docker compose config"
        return None, f"docker compose config fallo: {r.stderr.strip()}"

    # Respaldo estatico mediante PyYAML cuando el demonio Docker no esta instalado localmente
    datos = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
    return datos, "yaml estatico"


def composicion_valida() -> tuple[bool, str]:
    datos, modo = _cargar_compose()
    if not isinstance(datos, dict):
        return False, modo
    servicios = datos.get("services", {})
    if len(servicios) < 2:
        return False, f"se requieren al menos 2 servicios; hay {len(servicios)}"
    for nombre, cfg in servicios.items():
        img = str(cfg.get("image", ""))
        if not img or img.endswith(":latest") or ":" not in img:
            return False, f"servicio {nombre} sin etiqueta explicita de version ({img!r})"
    tiene_depends = any(cfg.get("depends_on") for cfg in servicios.values())
    if not tiene_depends:
        return False, "ningun servicio declara depends_on"
    return True, f"{len(servicios)} servicios con etiquetas explicitas y depends_on ({modo})"


def readme_con_secciones() -> tuple[bool, str]:
    ruta = Path("README.md")
    if not ruta.is_file():
        return False, "no existe README.md"
    titulos = set(re.findall(r"(?m)^## (.+)$", ruta.read_text(encoding="utf-8")))
    faltan = [s for s in SECCIONES_README if s not in titulos]
    if faltan:
        return False, f"faltan secciones H2: {faltan}"
    return True, f"las {len(SECCIONES_README)} secciones obligatorias estan presentes"


def variables_documentadas() -> tuple[bool, str]:
    env_ex = Path(".env.example")
    readme = Path("README.md")
    if not env_ex.is_file() or not readme.is_file():
        return False, "falta .env.example o README.md"
    vars_env = re.findall(r"(?m)^([A-Z][A-Z0-9_]*)=", env_ex.read_text(encoding="utf-8"))
    txt_readme = readme.read_text(encoding="utf-8")
    faltan = [v for v in vars_env if v not in txt_readme]
    if faltan:
        return False, f"variables sin documentar en README.md: {faltan}"
    return True, f"documentadas las {len(vars_env)} variables de .env.example"


def archivos_existentes() -> tuple[bool, str]:
    readme = Path("README.md")
    if not readme.is_file():
        return False, "no existe README.md"
    texto = readme.read_text(encoding="utf-8")
    # Remover bloques cercados de codigo para inspeccionar citas inline de rutas
    sin_bloques = re.sub(r"```.*?```", "", texto, flags=re.S)
    candidatos = re.findall(r"`([^`\s]+)`", sin_bloques)
    vistas: set[str] = set()
    faltantes: list[str] = []
    for c in candidatos:
        limpio = c.rstrip(".,;:")
        if (
            limpio.startswith(("/", "http://", "https://", "-", "--"))
            or limpio in PERMITIDAS_NO_VERSIONADAS
            or any(ch in limpio for ch in "{}*<>=")
        ):
            continue
        if "/" in limpio or limpio.endswith(EXTENSIONES_ARCHIVO):
            vistas.add(limpio)
            if not Path(limpio).exists():
                faltantes.append(limpio)
    if not vistas:
        return False, "README.md no cita archivos del repositorio"
    if faltantes:
        return False, f"el README cita archivos que no existen: {sorted(set(faltantes))}"
    return True, f"existen los {len(vistas)} archivos que cita"


def puertos_documentados() -> tuple[bool, str]:
    compose_path = Path("compose.yaml")
    readme = Path("README.md")
    if not compose_path.is_file() or not readme.is_file():
        return False, "falta compose.yaml o README.md"
    puertos = sorted(set(re.findall(r'"(\d+):\d+"', compose_path.read_text(encoding="utf-8"))))
    txt = readme.read_text(encoding="utf-8")
    faltan = [p for p in puertos if p not in txt]
    if faltan:
        return False, f"puertos sin documentar: {faltan}"
    return True, f"el README documenta los puertos {puertos}"


def revision_valida() -> tuple[bool, str]:
    ruta = Path("docs/verificacion_cruzada.md")
    if not ruta.is_file():
        return False, "no existe docs/verificacion_cruzada.md"
    texto = ruta.read_text(encoding="utf-8")

    for req in ("Revisor:", "Repositorio revisado:", "Fecha:", "Se siguió únicamente: README.md"):
        if req not in texto:
            return False, f"falta encabezado obligatorio '{req}'"

    fallas_vc: set[str] = set()
    for i in range(1, 7):
        c = f"VC-{i}"
        m = re.search(rf"(?m)^- {c} \([^)]*\): (PASA|FALLA) - .+$", texto)
        if not m:
            return False, f"falta o tiene formato invalido el criterio {c}"
        if m.group(1) == "FALLA":
            fallas_vc.add(c)

    hallazgos = re.findall(r"(?m)^- Hallazgo \d+ \((VC-\d)\): .+\n  Decisión: (?:aceptado|rechazado|aplazado) - .+$", texto)
    lineas_h = re.findall(r"(?m)^- Hallazgo \d+", texto)
    if len(hallazgos) != len(lineas_h):
        return False, "hay hallazgos sin linea inmediata '  Decisión: <estado> - <motivo>'"
    if not hallazgos and "Sin hallazgos" not in texto:
        return False, "sin hallazgos declarados debe contener 'Sin hallazgos'"
    no_cubiertas = fallas_vc - set(hallazgos)
    if no_cubiertas:
        return False, f"criterios FALLA sin hallazgo asociado: {sorted(no_cubiertas)}"

    return True, f"6 criterios VC verificados y {len(hallazgos)} hallazgo(s) con decision"


def sin_secretos() -> tuple[bool, str]:
    r = subprocess.run([sys.executable, "buscar_secretos.py"], capture_output=True, text=True)
    if r.returncode != 0:
        return False, "buscar_secretos.py reporto fallas"
    return True, "buscar_secretos.py sin fugas"


def main() -> int:
    checks = [
        ("ENT-1", composicion_valida),
        ("ENT-2", readme_con_secciones),
        ("ENT-3", variables_documentadas),
        ("ENT-4", archivos_existentes),
        ("ENT-5", puertos_documentados),
        ("ENT-6", revision_valida),
        ("ENT-7", sin_secretos),
    ]
    cumplidas = 0
    for cid, fn in checks:
        ok, det = fn()
        if ok:
            cumplidas += 1
        print(f"{'PASA' if ok else 'FALLA'} {cid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
