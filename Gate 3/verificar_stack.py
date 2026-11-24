"""Verificador del stack compuesto con Docker Compose (Bloque 38.2)."""

import json
import subprocess
import sys
import httpx

from casos import CASOS, ejecutar_caso


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    resultados: list[tuple[str, bool, str]] = []

    cfg = _run(["docker", "compose", "config", "--quiet"])
    ok_1 = cfg.returncode == 0
    resultados.append(("STK-1", ok_1, "compose.yaml valido" if ok_1 else cfg.stderr.strip()))
    if not ok_1:
        for rid, ok, det in resultados:
            print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
        print("0 de 7 comprobaciones cumplidas")
        return 1

    try:
        up = _run(["docker", "compose", "up", "-d", "--build", "--wait", "--wait-timeout", "120"])
        ok_2 = up.returncode == 0
        resultados.append(("STK-2", ok_2, "stack levantado con --wait" if ok_2 else up.stderr.strip()[:200]))
        if not ok_2:
            for rid, ok, det in resultados:
                print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
            print("1 de 7 comprobaciones cumplidas")
            return 1

        ps = _run(["docker", "compose", "ps", "--format", "json"])
        servicios = [json.loads(ln) for ln in ps.stdout.splitlines() if ln.strip()]
        ok_3 = len(servicios) >= 2 and all(s.get("Health", "").lower() == "healthy" for s in servicios)
        resultados.append(("STK-3", ok_3, f"{len(servicios)} servicios healthy" if ok_3 else f"estados: {[s.get('Health') for s in servicios]}"))

        r4 = httpx.get("http://127.0.0.1:8000/salud", timeout=5.0)
        resultados.append(("STK-4", r4.status_code == 200, f"API /salud={r4.status_code}"))

        r5 = httpx.get(
            "http://127.0.0.1:8080/preguntar",
            params={"texto": "Cual es el precio de referencia del Paracetamol 500 mg?"},
            timeout=5.0,
        )
        ok_5 = r5.status_code == 200 and "fuentes" in r5.json()
        resultados.append(("STK-5", ok_5, f"Interfaz /preguntar={r5.status_code}"))

        fallidos = []
        with httpx.Client(base_url="http://127.0.0.1:8000", timeout=5.0) as cli:
            for c in CASOS:
                ok, st, _ = ejecutar_caso(cli, c)
                if not ok:
                    fallidos.append(f"{c['id']}({st})")
        resultados.append(("STK-6", len(fallidos) == 0, f"{len(CASOS)} casos OK" if not fallidos else f"fallan: {fallidos}"))
    finally:
        _run(["docker", "compose", "down"])

    ps_post = _run(["docker", "compose", "ps", "-q"]).stdout.strip()
    resultados.append(("STK-7", ps_post == "", "apagado limpio sin contenedores residuales" if ps_post == "" else f"quedan: {ps_post}"))

    cumplidas = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
