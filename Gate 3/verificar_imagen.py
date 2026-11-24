"""Verificador en tiempo de ejecucion de la imagen Docker de la API (Bloque 37.3)."""

import subprocess
import sys
import time
import httpx

from casos import CASOS, ejecutar_caso

CONTENEDOR = "verificacion-imagen-cenabast"
PUERTO = 8099


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: python verificar_imagen.py <imagen:version>")
        return 2
    imagen = sys.argv[1]
    resultados: list[tuple[str, bool, str]] = []

    insp = _run(["docker", "image", "inspect", imagen])
    ok_1 = insp.returncode == 0
    resultados.append(("IMG-1", ok_1, f"imagen {imagen} presente" if ok_1 else f"imagen {imagen} no encontrada"))
    if not ok_1:
        for rid, ok, det in resultados:
            print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
        print(f"0 de 6 comprobaciones cumplidas")
        return 1

    _run(["docker", "rm", "-f", CONTENEDOR])
    try:
        arr = _run(["docker", "run", "-d", "--name", CONTENEDOR, "-p", f"{PUERTO}:8000", imagen])
        if arr.returncode != 0:
            print(f"FALLA al arrancar contenedor: {arr.stderr.strip()}")
            return 1

        # IMG-2: /salud responde 200 en <= 20s
        ok_2 = False
        for _ in range(40):
            try:
                r = httpx.get(f"http://127.0.0.1:{PUERTO}/salud", timeout=1.0)
                if r.status_code == 200:
                    ok_2 = True
                    break
            except httpx.HTTPError:
                pass
            time.sleep(0.5)
        resultados.append(("IMG-2", ok_2, "/salud respondio 200" if ok_2 else "/salud no respondio 200 en 20s"))

        # IMG-3: usuario no-root
        uid = _run(["docker", "exec", CONTENEDOR, "id", "-u"]).stdout.strip()
        resultados.append(("IMG-3", bool(uid) and uid != "0", f"uid={uid}"))

        # IMG-4: sin .env ni .git dentro de /app
        archivos = set(_run(["docker", "exec", CONTENEDOR, "ls", "-a", "/app"]).stdout.splitlines())
        ok_4 = ".env" not in archivos and ".git" not in archivos
        resultados.append(("IMG-4", ok_4, "sin .env ni .git en /app" if ok_4 else f"encontrados archivos prohibidos en /app"))

        # IMG-5: todos los CASOS pasan
        fallidos = []
        with httpx.Client(base_url=f"http://127.0.0.1:{PUERTO}", timeout=5.0) as cli:
            for c in CASOS:
                ok, st, _ = ejecutar_caso(cli, c)
                if not ok:
                    fallidos.append(f"{c['id']}({st})")
        resultados.append(("IMG-5", len(fallidos) == 0, f"{len(CASOS)} casos OK" if not fallidos else f"fallan: {fallidos}"))

        # IMG-6: estado healthy
        ok_6 = False
        for _ in range(40):
            st = _run(["docker", "inspect", "--format", "{{.State.Health.Status}}", CONTENEDOR]).stdout.strip()
            if st == "healthy":
                ok_6 = True
                break
            time.sleep(0.5)
        resultados.append(("IMG-6", ok_6, "contenedor healthy" if ok_6 else "contenedor no alcanzo healthy en 20s"))
    finally:
        _run(["docker", "rm", "-f", CONTENEDOR])

    cumplidas = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
