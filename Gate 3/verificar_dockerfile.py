"""Verificador estatico de 7 reglas sobre Dockerfile y .dockerignore (Bloque 37.3)."""

from pathlib import Path
import re
import sys

PATRON_SECRETO = re.compile(r"KEY|TOKEN|SECRET|PASSWORD", re.I)


def verificar_dockerfile(ruta: Path) -> list[tuple[str, bool, str]]:
    resultados: list[tuple[str, bool, str]] = []
    if not ruta.is_file():
        return [("DF-0", False, f"No existe {ruta}")]

    lineas_crudas = ruta.read_text(encoding="utf-8").splitlines()
    # Unir lineas continuadas con \
    instrucciones: list[tuple[int, str, str]] = []
    buf = ""
    inicio = 1
    for i, raw in enumerate(lineas_crudas, 1):
        limpia = raw.strip()
        if not limpia or limpia.startswith("#"):
            continue
        if not buf:
            inicio = i
        if limpia.endswith("\\"):
            buf += limpia[:-1] + " "
        else:
            completa = (buf + limpia).strip()
            partes = completa.split(None, 1)
            cmd = partes[0].upper()
            arg = partes[1] if len(partes) > 1 else ""
            instrucciones.append((inicio, cmd, arg))
            buf = ""

    # DF-1: FROM con etiqueta explicita y distinta de latest
    froms = [arg for _, cmd, arg in instrucciones if cmd == "FROM"]
    ok_df1 = bool(froms) and all(":" in f.split()[0] and not f.split()[0].endswith(":latest") for f in froms)
    resultados.append(("DF-1", ok_df1, f"FROM={froms}"))

    # DF-2: COPY requirements antes de RUN pip install, y COPY de codigo despues
    idx_req = [idx for idx, (_, cmd, arg) in enumerate(instrucciones) if cmd == "COPY" and "requirements" in arg]
    idx_pip = [idx for idx, (_, cmd, arg) in enumerate(instrucciones) if cmd == "RUN" and "pip install" in arg]
    idx_other_copy = [idx for idx, (_, cmd, arg) in enumerate(instrucciones) if cmd == "COPY" and "requirements" not in arg]
    ok_df2 = (
        bool(idx_req)
        and bool(idx_pip)
        and bool(idx_other_copy)
        and min(idx_req) < min(idx_pip)
        and min(idx_other_copy) > min(idx_pip)
    )
    resultados.append(("DF-2", ok_df2, "orden de capas cache-friendly verificado" if ok_df2 else "orden COPY/RUN invalido"))

    # DF-3: CMD o ENTRYPOINT escucha en 0.0.0.0
    cmds = [arg for _, cmd, arg in instrucciones if cmd in ("CMD", "ENTRYPOINT")]
    ok_df3 = any("0.0.0.0" in c for c in cmds)
    resultados.append(("DF-3", ok_df3, "escucha en 0.0.0.0" if ok_df3 else "falta host 0.0.0.0 en CMD/ENTRYPOINT"))

    # DF-4: al menos un USER y el ultimo no es root ni 0
    users = [arg.split()[0].strip() for _, cmd, arg in instrucciones if cmd == "USER"]
    ok_df4 = bool(users) and users[-1].lower() not in ("root", "0")
    resultados.append(("DF-4", ok_df4, f"ultimo USER={users[-1] if users else 'ninguno'}"))

    # DF-5: sin nombres de secretos en ENV o ARG
    malas = []
    for _, cmd, arg in instrucciones:
        if cmd in ("ENV", "ARG"):
            for token in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*=?", arg):
                if PATRON_SECRETO.search(token):
                    malas.append(f"{cmd} {token}")
    resultados.append(("DF-5", len(malas) == 0, "sin secretos en ENV/ARG" if not malas else f"encontrados: {malas}"))

    # DF-6: .dockerignore en el directorio del Dockerfile con .env, .git y .venv
    dockerignore = ruta.parent / ".dockerignore"
    if not dockerignore.is_file():
        dockerignore = Path(".dockerignore")
    if dockerignore.is_file():
        entradas = {ln.strip() for ln in dockerignore.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")}
        requeridas = {".env", ".git", ".venv"}
        faltan = sorted(requeridas - entradas)
        ok_df6 = len(faltan) == 0
        det_df6 = f"{dockerignore} excluye .env, .git, .venv" if ok_df6 else f"faltan en {dockerignore}: {faltan}"
    else:
        ok_df6 = False
        det_df6 = "no existe .dockerignore"
    resultados.append(("DF-6", ok_df6, det_df6))

    # DF-7: HEALTHCHECK presente
    ok_df7 = any(cmd == "HEALTHCHECK" for _, cmd, _ in instrucciones)
    resultados.append(("DF-7", ok_df7, "HEALTHCHECK declarado" if ok_df7 else "falta HEALTHCHECK"))

    return resultados


def main() -> int:
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Dockerfile")
    resultados = verificar_dockerfile(ruta)
    cumplidas = 0
    for rid, ok, detalle in resultados:
        if ok:
            cumplidas += 1
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {detalle}")
    print(f"{cumplidas} de {len(resultados)} reglas cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
