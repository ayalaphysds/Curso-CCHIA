"""Prueba en frio de 5 pasos sobre un clon limpio del repositorio (Bloque 44.3)."""

import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
import httpx

import contar_friccion as cf


def _puerto_libre(puerto: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", puerto)) != 0


def _detener_proceso(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def _extraer_uvicorn(texto_readme: str) -> str:
    secs = cf.secciones(texto_readme)
    arr = next((v for k, v in secs.items() if "arrancar" in k), "")
    for bloque in re.findall(r"```(?:[a-zA-Z0-9_-]*)\n(.*?)```", arr, flags=re.S):
        for linea in bloque.splitlines():
            limpia = linea.strip()
            if "uvicorn" in limpia and not limpia.startswith("#"):
                return limpia
    return "python -m uvicorn servicio.main:app --host 127.0.0.1 --port 8000"


def main() -> int:
    if not _puerto_libre(8000):
        print("FALLA FRIO-0: el puerto 8000 esta ocupado; deten el servicio previo antes de probar en frio")
        print("0 de 5 pasos cumplidos")
        return 1

    raiz_git = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if not raiz_git:
        print("FALLA FRIO-1: no se detecto repositorio Git")
        print("0 de 5 pasos cumplidos")
        return 1

    cwd_abs = Path.cwd().resolve()
    rel_sub = cwd_abs.relative_to(Path(raiz_git).resolve())
    resultados: list[tuple[str, bool, str]] = []

    with tempfile.TemporaryDirectory() as tmp:
        clon = Path(tmp) / "proyecto"
        r_clone = subprocess.run(["git", "clone", "--quiet", raiz_git, str(clon)], capture_output=True, text=True)
        trabajo = clon / rel_sub
        r_ls = subprocess.run(["git", "ls-files"], cwd=trabajo, capture_output=True, text=True)
        ok_1 = r_clone.returncode == 0 and bool(r_ls.stdout.strip()) and (trabajo / "README.md").is_file()
        resultados.append(("FRIO-1", ok_1, f"clon limpio en {rel_sub} ({len(r_ls.stdout.splitlines())} archivos)" if ok_1 else "clon incompleto o Gate 3 sin commit"))
        if not ok_1:
            for rid, ok, det in resultados:
                print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
            print("0 de 5 pasos cumplidos")
            return 1

        # FRIO-2: verificar requisitos e instalacion reproducible
        req_dev = trabajo / "requirements-dev.txt"
        r_chk = subprocess.run(
            [sys.executable, "-c", "import fastapi, uvicorn, pydantic, httpx, pytest, yaml"],
            cwd=trabajo,
            capture_output=True,
            text=True,
        )
        ok_2 = req_dev.is_file() and r_chk.returncode == 0
        resultados.append(("FRIO-2", ok_2, "entorno y dependencias verificadas en clon limpio" if ok_2 else r_chk.stderr.strip()))

        # FRIO-3: pruebas en clon limpio
        r_test = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=trabajo, capture_output=True, text=True)
        ok_3 = r_test.returncode == 0
        resumen_t = r_test.stdout.strip().splitlines()[-1] if r_test.stdout.strip() else "sin salida"
        resultados.append(("FRIO-3", ok_3, resumen_t))

        # FRIO-4: arranque real con uvicorn del README
        cmd_str = _extraer_uvicorn((trabajo / "README.md").read_text(encoding="utf-8"))
        partes = cmd_str.split()
        if partes and partes[0] in ("python", "python3"):
            partes[0] = sys.executable
        elif partes and partes[0] == "uvicorn":
            partes = [sys.executable, "-m"] + partes

        env = os.environ.copy()
        env.pop("GEMINI_API_KEY", None)
        env["MODELO"] = "simulado"
        proc = subprocess.Popen(partes, cwd=trabajo, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            ok_4 = False
            for _ in range(40):
                try:
                    r = httpx.get("http://127.0.0.1:8000/salud", timeout=1.0)
                    if r.status_code == 200:
                        ok_4 = True
                        break
                except httpx.HTTPError:
                    pass
                time.sleep(0.5)
            resultados.append(("FRIO-4", ok_4, "servidor vivo en http://127.0.0.1:8000/salud" if ok_4 else "uvicorn no respondio en 20s"))

            # FRIO-5: consulta real verificando cita CENABAST
            ok_5 = False
            det_5 = "servidor no disponible"
            if ok_4:
                r5 = httpx.post(
                    "http://127.0.0.1:8000/consultas",
                    json={"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"},
                    timeout=5.0,
                )
                datos = r5.json() if r5.status_code == 200 else {}
                ok_5 = r5.status_code == 200 and "cenabast_catalogo_precios_referencia_2026.md" in datos.get("fuentes", [])
                det_5 = f"HTTP {r5.status_code}, fuentes={datos.get('fuentes')}"
            resultados.append(("FRIO-5", ok_5, det_5))
        finally:
            _detener_proceso(proc)

    cumplidos = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidos} de {len(resultados)} pasos cumplidos")
    return 0 if cumplidos == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
