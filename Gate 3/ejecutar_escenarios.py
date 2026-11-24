"""Ejecutor end-to-end de ESCENARIOS sobre API y Interfaz HTTP (Bloque 40)."""

import sys
import httpx

from escenarios import ESCENARIOS

DESTINOS = {
    "api": "http://127.0.0.1:8000",
    "interfaz": "http://127.0.0.1:8080",
}


def correr(destinos: dict[str, str] | None = None) -> list[dict]:
    urls = destinos or DESTINOS
    resultados: list[dict] = []
    with httpx.Client(timeout=5.0) as cliente:
        for esc in ESCENARIOS:
            base = urls[esc["destino"]].rstrip("/")
            url = base + esc["ruta"]
            kwargs: dict = {}
            if "json" in esc:
                kwargs["json"] = esc["json"]
            if "params" in esc:
                kwargs["params"] = esc["params"]

            motivos: list[str] = []
            try:
                r = cliente.request(esc["metodo"], url, **kwargs)
                estado = r.status_code
                cuerpo = r.text
            except httpx.HTTPError as exc:
                estado = 0
                cuerpo = ""
                motivos.append(f"error de conexion: {type(exc).__name__}")

            if estado != esc["estado"]:
                motivos.append(f"estado esperado={esc['estado']} obtenido={estado}")
            for esperado in esc.get("contiene", []):
                if esperado not in cuerpo:
                    motivos.append(f"falta texto {esperado!r}")

            resultados.append(
                {
                    "id": esc["id"],
                    "categoria": esc["categoria"],
                    "destino": esc["destino"],
                    "estado": estado,
                    "motivos": motivos,
                }
            )
    return resultados


def firma(resultados: list[dict]) -> list[tuple[str, int, tuple[str, ...]]]:
    return [(r["id"], r["estado"], tuple(r["motivos"])) for r in resultados]


def main() -> int:
    dos_veces = "--dos-veces" in sys.argv
    primera = correr()
    cumplidos = sum(1 for r in primera if not r["motivos"])
    for r in primera:
        etiqueta = "PASA" if not r["motivos"] else "FALLA"
        det = "ok" if not r["motivos"] else "; ".join(r["motivos"])
        print(f"{etiqueta} {r['id']} [{r['categoria']}] ({r['destino']}): {det}")
    print(f"Escenarios: {cumplidos} de {len(primera)} cumplidos")

    if dos_veces:
        segunda = correr()
        iguales = firma(primera) == firma(segunda)
        print(f"Repetibilidad (--dos-veces): {'IGUALES' if iguales else 'DIFERENTES'}")
        if not iguales:
            return 1

    return 0 if cumplidos == len(primera) else 1


if __name__ == "__main__":
    sys.exit(main())
