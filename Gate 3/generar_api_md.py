"""Genera o comprueba docs/api.md ejecutando EJEMPLOS contra TestClient(app) (Bloque 45.1)."""

import hashlib
import json
from pathlib import Path
import sys
from fastapi.testclient import TestClient

from ejemplos_api import EJEMPLOS
from servicio.main import app

DESTINO = Path("docs/api.md")


def _normalizar_cuerpo(datos):
    if isinstance(datos, dict) and "trace_id" in datos:
        copia = dict(datos)
        copia["trace_id"] = "trace-ejemplo"
        return copia
    return datos


def renderizar() -> tuple[str, int]:
    cliente = TestClient(app, raise_server_exceptions=False)
    registros = []
    ok_total = 0

    for ej in EJEMPLOS:
        kwargs = {"json": ej["json"]} if "json" in ej else {}
        r = cliente.request(ej["metodo"], ej["ruta"], **kwargs)
        cuerpo = _normalizar_cuerpo(r.json())
        ok = r.status_code == ej["estado"]
        if ok:
            ok_total += 1
        registros.append((ej, r.status_code, cuerpo, ok))

    huella = hashlib.sha256(
        json.dumps([(e["id"], st, c) for e, st, c, _ in registros], sort_keys=True, ensure_ascii=True).encode("utf-8")
    ).hexdigest()[:12]

    lineas = [
        "# Referencia de Endpoints — API CENABAST",
        "",
        f"Huella de ejemplos ejecutados: `{huella}`",
        f"Ejemplos verificados: {ok_total} de {len(EJEMPLOS)}",
        "",
        "Documento generado automáticamente ejecutando `ejemplos_api.py` contra `servicio.main:app`.",
        "",
    ]

    for ej, estado, cuerpo, _ in registros:
        lineas.append(f"## {ej['id']} — {ej['titulo']}")
        lineas.append("")
        lineas.append(f"- **Petición:** `{ej['metodo']} {ej['ruta']}`")
        if "json" in ej:
            lineas.append(f"- **Cuerpo JSON:** `{json.dumps(ej['json'], ensure_ascii=False)}`")
        lineas.append(f"- **Respuesta HTTP:** `{estado}`")
        lineas.append("")
        lineas.append("```json")
        lineas.append(json.dumps(cuerpo, ensure_ascii=False, indent=2))
        lineas.append("```")
        lineas.append("")

    return "\n".join(lineas), ok_total


def main() -> int:
    contenido, ok_total = renderizar()
    if "--comprobar" in sys.argv:
        if not DESTINO.is_file():
            print(f"FALLA: no existe {DESTINO}")
            return 1
        actual = DESTINO.read_text(encoding="utf-8")
        if actual != contenido:
            print(f"FALLA: {DESTINO} esta desactualizado respecto a servicio.main:app")
            return 1
        print(f"PASA: {DESTINO} coincide con los ejemplos ejecutados")
        print(f"{ok_total} de {len(EJEMPLOS)} comprobaciones cumplidas")
        return 0

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(contenido, encoding="utf-8")
    print(f"Escrito: {DESTINO} ({ok_total} de {len(EJEMPLOS)} ejemplos)")
    return 0 if ok_total == len(EJEMPLOS) else 1


if __name__ == "__main__":
    sys.exit(main())
