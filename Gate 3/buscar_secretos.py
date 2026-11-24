"""Detector de secretos en repositorio, .env.example e imagen Docker (Bloque 38.1)."""

import json
from pathlib import Path
import re
import subprocess
import sys

CLAVE_GOOGLE = re.compile(r"AIza[0-9A-Za-z_\-]{35}")
NOMBRE_SECRETO = r"(?:GEMINI_API_KEY|API_KEY|SECRET_KEY|ACCESS_TOKEN|AUTH_TOKEN|PASSWORD|DB_PASSWORD)"
ASIGNACION = re.compile(
    rf"(?m)^[ \t]*(?:export[ \t]+)?{NOMBRE_SECRETO}[ \t]*=[ \t]*['\"]?(?![ \t]*(?:$|#)|\$\{{|\<|tu_|your_|ejemplo|example|placeholder|\[)([^\s'\"#]+)",
    re.I,
)
ASIGNACION_PY = re.compile(
    rf"(?m)\b{NOMBRE_SECRETO}\s*=\s*['\"](?!\s*$|tu_|your_|ejemplo|example|placeholder|\[)([^'\"]{{12,}})['\"]",
    re.I,
)

IGNORAR_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "indice_gate2"}
EXTENSIONES_TEXTO = {".py", ".md", ".yaml", ".yml", ".txt", ".json", ".jsonl", ".toml", ".cfg", ".ini", ".sh", ".ps1", ""}


def archivos_del_repo(raiz: Path = Path(".")) -> list[Path]:
    encontrados: list[Path] = []
    for ruta in raiz.rglob("*"):
        if any(parte in IGNORAR_DIRS for parte in ruta.parts):
            continue
        if not ruta.is_file():
            continue
        if ruta.name == ".env" or ruta.name == "buscar_secretos.py":
            continue
        if ruta.suffix.lower() in EXTENSIONES_TEXTO:
            encontrados.append(ruta)
    return sorted(encontrados)


def verificar_repo(raiz: Path = Path(".")) -> list[tuple[str, bool, str]]:
    resultados: list[tuple[str, bool, str]] = []

    # SEC-1: sin claves ni asignaciones de secretos en archivos del repositorio
    hallazgos = []
    for ruta in archivos_del_repo(raiz):
        try:
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if CLAVE_GOOGLE.search(texto):
            hallazgos.append(f"{ruta} (clave Google)")
        elif ASIGNACION.search(texto) or ASIGNACION_PY.search(texto):
            # Excluir .env.example (se valida en SEC-4)
            if ruta.name != ".env.example":
                hallazgos.append(f"{ruta} (asignacion de secreto)")
    resultados.append(("SEC-1", len(hallazgos) == 0, "sin secretos en archivos" if not hallazgos else f"detectados: {hallazgos}"))

    # SEC-2: .env ignorado por git
    r_ign = subprocess.run(["git", "check-ignore", "-q", ".env"], capture_output=True)
    ok_2 = r_ign.returncode == 0
    resultados.append(("SEC-2", ok_2, ".env ignorado por Git" if ok_2 else ".env no esta en .gitignore"))

    # SEC-3: .env no rastreado por git
    r_ls = subprocess.run(["git", "ls-files", ".env"], capture_output=True, text=True)
    ok_3 = r_ls.returncode == 0 and not r_ls.stdout.strip()
    resultados.append(("SEC-3", ok_3, ".env fuera del indice Git" if ok_3 else ".env esta versionado en Git"))

    # SEC-4: .env.example existe y sus secretos estan vacios
    env_ex = raiz / ".env.example"
    if not env_ex.is_file():
        resultados.append(("SEC-4", False, "no existe .env.example"))
    else:
        txt = env_ex.read_text(encoding="utf-8")
        malos = []
        for linea in txt.splitlines():
            limpia = linea.strip()
            if not limpia or limpia.startswith("#") or "=" not in limpia:
                continue
            clave, valor = limpia.split("=", 1)
            if re.search(r"KEY|TOKEN|SECRET|PASSWORD", clave, re.I) and valor.strip():
                malos.append(clave.strip())
        resultados.append(("SEC-4", len(malos) == 0, ".env.example sin valores secretos" if not malos else f"secretos con valor: {malos}"))

    return resultados


def verificar_imagen_sin_secretos(imagen: str) -> tuple[str, bool, str]:
    insp = subprocess.run(["docker", "image", "inspect", imagen], capture_output=True, text=True)
    hist = subprocess.run(["docker", "history", "--no-trunc", imagen], capture_output=True, text=True)
    if insp.returncode != 0:
        return ("SEC-5", False, f"no se pudo inspeccionar imagen {imagen}")
    datos = json.loads(insp.stdout)
    env_list = "\n".join(datos[0].get("Config", {}).get("Env", []))
    combinado = env_list + "\n" + hist.stdout
    if CLAVE_GOOGLE.search(combinado) or ASIGNACION.search(combinado):
        return ("SEC-5", False, f"se detecto secreto en metadata o capas de {imagen}")
    return ("SEC-5", True, f"imagen {imagen} sin secretos en Config.Env ni history")


def main() -> int:
    resultados = verificar_repo()
    if len(sys.argv) > 1:
        resultados.append(verificar_imagen_sin_secretos(sys.argv[1]))

    cumplidas = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
